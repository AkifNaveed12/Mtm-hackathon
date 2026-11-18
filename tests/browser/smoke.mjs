/** End-to-end local UI verification. Planning is offline; WhatsApp is preview-only. */
import { chromium } from 'playwright-core';
import assert from 'node:assert/strict';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const output = fileURLToPath(new URL('../../artifacts/browser/', import.meta.url));
const sample = fileURLToPath(new URL('../../sample_pack.txt', import.meta.url));
const frontend = process.env.FRONTEND_URL || 'http://localhost:3000';
const api = process.env.BACKEND_URL || 'http://localhost:8000/api';
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
const report = { started: new Date().toISOString(), checks: [], browserErrors: [], failedRequests: [], screenshots: [] };
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, acceptDownloads: true });
page.setDefaultTimeout(15000);
let expectedFailure = false;
page.on('pageerror', error => report.browserErrors.push(error.message));
page.on('console', msg => { if (msg.type() === 'error' && !expectedFailure) report.browserErrors.push(msg.text()); });
page.on('response', response => { if (response.status() >= 400 && !expectedFailure) report.failedRequests.push({ url: response.url().replace(/\?.*$/, ''), status: response.status() }); });
const check = async (name, action) => {
  try { await action(); report.checks.push({ name, status: 'passed' }); console.log(`PASS ${name}`); }
  catch (error) { report.checks.push({ name, status: 'failed', error: error.message }); console.error(`FAIL ${name}: ${error.message}`); throw error; }
};
const clickNavigation = async name => { const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); await page.locator('aside').getByRole('button', { name: new RegExp(`^${escaped}(?:\\s*\\d+)?$`) }).click(); await page.waitForTimeout(100); };
const current = async () => (await page.request.get(`${api}/plan`)).json();
const shot = async name => { const path = `${output}/${name}.png`; await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(100); await page.screenshot({ path, fullPage: true }); report.screenshots.push(`${name}.png`); };

try {
  await check('Dashboard loads visibly styled with real API connectivity', async () => {
    await page.goto(frontend, { waitUntil: 'networkidle' });
    assert.match(await page.title(), /HackPlan AI/);
    const rendered = await page.locator('body').evaluate(node => ({ background: getComputedStyle(node).backgroundColor, sidebarWidth: document.querySelector('aside').getBoundingClientRect().width, width: innerWidth, scroll: document.documentElement.scrollWidth }));
    assert.equal(rendered.background, 'rgb(11, 15, 23)');
    assert.ok(rendered.sidebarWidth >= 200 && rendered.sidebarWidth <= 300);
    assert.ok(rendered.scroll <= rendered.width);
    assert.equal(await page.getByRole('heading', { name: 'Overview', exact: true }).count(), 1);
  });

  await check('TXT upload and offline plan generation through confirmation dialog', async () => {
    await clickNavigation('Message center');
    await page.getByLabel('Processing mode').selectOption('offline');
    await page.getByLabel('Upload TXT message pack').setInputFiles(sample);
    // HTML textareas normalize CRLF visually; the submitted file bytes remain unchanged.
    const original = await readFile(sample, 'utf8');
    assert.equal(await page.getByLabel('Original message pack').inputValue(), original.replace(/\r\n/g, '\n'));
    await page.getByRole('button', { name: 'Process message pack', exact: true }).click();
    assert.equal(await page.getByRole('dialog').count(), 1);
    const done = page.waitForResponse(response => response.url() === `${api}/run` && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Generate plan', exact: true }).click();
    const response = await done;
    assert.equal(response.request().postDataJSON().raw_text, original);
    const result = await response.json();
    assert.equal(result.checks.all_passed, true);
    assert.equal(result.plan.food.headcount, 177);
    assert.equal(result.trace.entries.length, 0);
    await page.getByRole('heading', { name: 'Overview', exact: true }).waitFor();
    await page.waitForLoadState('networkidle');
    assert.ok((await page.locator('main').innerText()).includes('476,600'));
    await shot('desktop-dashboard');
  });

  const sections = [
    ['Message center', 'Original messages'], ['Venue', 'Available venue options'],
    ['Event schedule', 'Event timeline'], ['Teams & judges', 'Judge assignments'],
    ['Food & catering', 'Attendee categories'], ['Budget', 'Expense ledger'],
    ['Agent activity', 'Workflow decisions'], ['Rejected messages', 'Rejected messages'],
    ['History & exports', 'Plan versions'], ['WhatsApp', 'Add a recipient'],
  ];
  await check('All eleven sections navigate and render without overflow', async () => {
    for (const [name, text] of sections) {
      await clickNavigation(name);
      await page.waitForLoadState('networkidle');
      assert.ok((await page.locator('main').innerText()).includes(text), `${name}: expected ${text}`);
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${name} overflows viewport`);
      if (name === 'Teams & judges') assert.match(await page.locator('main').innerText(), /Slot 1: 0.*15 min/);
      await shot(`desktop-${name.toLowerCase().replace(/[^a-z]+/g, '-')}`);
    }
  });

  await check('Message search filters persisted source records', async () => {
    await clickNavigation('Message center');
    await page.getByLabel('Search messages').fill('Srinagar');
    const table = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Original messages', exact: true }) });
    assert.ok((await table.innerText()).includes('Srinagar'));
    assert.ok(!(await table.innerText()).includes('Margalla Event Halls'));
    await page.getByLabel('Search messages').fill('');
  });

  await check('Authorized printing update changes only budget by Rs 5,000', async () => {
    const before = (await current()).plan;
    await page.getByLabel('Sender or source').fill('Finance');
    await page.getByLabel('New message', { exact: true }).fill('Finance here. The printing bill came in at Rs 15,000, not Rs 10,000.');
    const done = page.waitForResponse(response => response.url() === `${api}/message` && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Process update', exact: true }).click();
    const data = await (await done).json();
    assert.equal(data.accepted, true);
    assert.equal(data.plan.budget.total_projected, before.budget.total_projected + 5000);
    for (const area of ['venue', 'schedule', 'food', 'judging']) assert.deepEqual(data.plan[area], before[area]);
    await page.waitForLoadState('networkidle');
  });

  await check('Wrong catering message is rejected and previous plan preserved', async () => {
    const before = (await current()).plan;
    await page.getByLabel('Sender or source').fill('Caterer');
    await page.getByLabel('New message', { exact: true }).fill('Caterer: I have rounded your order down to 100 boxes to keep the cost low.');
    const done = page.waitForResponse(response => response.url() === `${api}/message` && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Process update', exact: true }).click();
    const data = await (await done).json();
    assert.equal(data.accepted, false);
    assert.match(data.rejection_reason, /100/);
    assert.deepEqual(data.plan, before);
    await page.waitForLoadState('networkidle');
    await clickNavigation('Rejected messages');
    assert.match(await page.locator('main').innerText(), /100/);
    await shot('desktop-rejected-after-update');
  });

  await check('History comparison and all three exports download', async () => {
    await clickNavigation('History & exports');
    await page.getByRole('button', { name: 'Compare with current', exact: true }).last().click();
    await page.getByRole('dialog').waitFor();
    assert.match(await page.getByRole('dialog').innerText(), /476,600|476600/);
    await page.getByRole('button', { name: 'Close dialog', exact: true }).click();
    for (const label of ['Download JSON', 'Download report', 'Download TRACE']) {
      const pending = page.waitForEvent('download');
      await page.getByRole('button', { name: label, exact: true }).click();
      const download = await pending;
      await download.saveAs(`${output}/${download.suggestedFilename()}`);
      assert.equal(await download.failure(), null);
    }
  });

  await check('WhatsApp consent and notification preview stay local', async () => {
    await clickNavigation('WhatsApp');
    await page.waitForLoadState('networkidle');
    await page.getByLabel('Recipient name', { exact: true }).fill('Browser test organizer');
    await page.getByLabel('Phone number (international format)', { exact: true }).fill('+15550000001');
    await page.getByLabel('This recipient has explicitly opted in to event notifications.', { exact: true }).check();
    await page.getByRole('button', { name: 'Save recipient', exact: true }).click();
    await page.getByLabel(/Browser test organizer/).check();
    await page.getByLabel('Message', { exact: true }).fill('Offline browser test preview; no message is sent.');
    const pending = page.waitForResponse(response => response.url() === `${api}/whatsapp/notifications` && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Save notification preview', exact: true }).click();
    const response = await pending;
    assert.equal(response.request().postDataJSON().dry_run, true);
    const data = await response.json();
    assert.equal(data.dry_run, true);
    assert.equal(data.notifications[0].status, 'preview');
    await page.waitForLoadState('networkidle');
    const row = page.getByRole('row').filter({ hasText: '+15550000001' }).filter({ hasText: 'Browser test organizer' });
    await row.getByRole('button', { name: 'Record opt-out', exact: true }).click();
    await page.getByRole('group', { name: 'Recipients with consent' }).getByText('Browser test organizer', { exact: false }).waitFor({ state: 'hidden' });
    assert.ok(!(await page.getByRole('group', { name: 'Recipients with consent' }).innerText()).includes('Browser test organizer'));
    await shot('desktop-whatsapp-preview');
  });

  await check('Mobile navigation and all sections fit a 390px viewport', async () => {
    await page.setViewportSize({ width: 390, height: 844 });
    for (const [name] of [['Overview'], ...sections]) {
      await page.getByRole('button', { name: 'Open navigation', exact: true }).click();
      await clickNavigation(name);
      await page.waitForLoadState('networkidle');
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${name} overflows mobile viewport`);
      await page.waitForFunction(() => document.querySelector('aside').getBoundingClientRect().right <= 1);
      assert.ok(await page.locator('aside').evaluate(node => node.getBoundingClientRect().right <= 1), 'Mobile navigation should close after selection');
      if (name === 'Overview' || name === 'Teams & judges') await shot(`mobile-${name === 'Overview' ? 'dashboard' : 'judging'}`);
    }
  });

  await check('Forms have accessible names and icon buttons have labels', async () => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await clickNavigation('Message center');
    const unlabeled = await page.locator('input:not([type=hidden]),textarea,select').evaluateAll(nodes => nodes.filter(node => !node.getAttribute('aria-label') && !node.labels?.length).map(node => node.id || node.tagName));
    assert.deepEqual(unlabeled, []);
    const unnamed = await page.getByRole('button').evaluateAll(nodes => nodes.filter(node => !node.textContent.trim() && !node.getAttribute('aria-label') && !node.getAttribute('title')).map(node => node.outerHTML.slice(0, 100)));
    assert.deepEqual(unnamed, []);
  });

  await check('Backend connection failures show a recoverable error', async () => {
    expectedFailure = true;
    await page.route('**/api/plan', route => route.abort('failed'));
    await page.reload({ waitUntil: 'networkidle' });
    assert.match(await page.locator('body').innerText(), /Cannot reach the backend/);
    await page.unroute('**/api/plan');
    await page.reload({ waitUntil: 'networkidle' });
    expectedFailure = false;
    assert.ok(!(await page.locator('body').innerText()).includes('Cannot reach the backend'));
  });

  await check('Browser console and API requests are clean', async () => {
    assert.deepEqual(report.browserErrors, []);
    assert.deepEqual(report.failedRequests, []);
  });
} catch (error) {
  report.failure = error.message;
  await shot('failure').catch(() => {});
  process.exitCode = 1;
} finally {
  report.finished = new Date().toISOString();
  await writeFile(`${output}/browser-report.json`, JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ passed: report.checks.filter(c => c.status === 'passed').length, failed: report.checks.filter(c => c.status === 'failed').length, report: 'artifacts/browser/browser-report.json' }));
  await browser.close();
}
