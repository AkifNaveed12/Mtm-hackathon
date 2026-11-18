import { chromium } from 'playwright-core';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const output = fileURLToPath(new URL('../../artifacts/browser/', import.meta.url));
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const errors = [];
  page.on('pageerror', err => errors.push(err.message));
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  await page.goto(process.env.FRONTEND_URL || 'http://localhost:3000', { waitUntil: 'networkidle' });
  await page.screenshot({ path: `${output}/desktop-inspect.png`, fullPage: true });
  const report = {
    title: await page.title(),
    headings: await page.getByRole('heading').allTextContents(),
    buttons: await page.getByRole('button').allTextContents(),
    links: await page.getByRole('link').allTextContents(),
    controls: await page.locator('input,select,textarea').evaluateAll(nodes => nodes.map(n => ({tag:n.tagName,type:n.getAttribute('type'),label:n.getAttribute('aria-label'),placeholder:n.getAttribute('placeholder'),id:n.id}))),
    errors,
    rendered: await page.locator('body').evaluate(node => ({ background:getComputedStyle(node).backgroundColor,font:getComputedStyle(node).fontFamily,scrollWidth:document.documentElement.scrollWidth,windowWidth:innerWidth })),
  };
  await writeFile(`${output}/inspect.json`, JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
} finally {
  await browser.close();
}
