# HackPlan AI frontend

The Next.js dashboard uses the local FastAPI backend. It does not automatically generate a plan or send notifications on page load.

From the repository root, start the backend in a PowerShell terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend in another terminal:

```powershell
cd D:\mtmm\Mtm-hackathon\frontend
npm install
npm run dev
```

Open http://localhost:3000. To run the compiled frontend:

```powershell
npm run build
npm start -- --hostname 127.0.0.1 --port 3000
```

Use one frontend server on port 3000 at a time. Stop the development server before building or starting production mode.

For a different backend address, copy `.env.example` to `.env.local` and set `NEXT_PUBLIC_API_URL`. This value is public: never put provider keys in it. The optional `NEXT_PUBLIC_ENABLE_AGENTATION=true` enables the existing annotation tool in development only. Fonts use the system sans-serif stack, so builds do not need Google Fonts connectivity.

In Message center, select **Offline parser** for deterministic processing without provider calls, or require the configured live provider. The UI shows extracted facts, constraint warnings, plan versions, actual model traces, and provider-reported usage. WhatsApp notification controls only save dry-run previews.

If the backend requires `ORGANIZER_API_KEY`, open **Organizer access** and enter the local organizer key. The frontend retains it in memory for the current page session; no browser storage is used.

Checks:

```powershell
npm run lint
npm run build
npm audit --omit=dev
```

Source formatting is available with `npm run format`. Browser integration tests live under the root `tests/browser/` directory. See the root completion report for executed checks and remaining external integration blockers.
