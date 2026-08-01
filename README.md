# Lead Router Agent

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![OpenAI SDK](https://img.shields.io/badge/OpenAI_SDK-412991?style=flat&logo=openai&logoColor=white)
![Gmail API](https://img.shields.io/badge/Gmail_API-EA4335?style=flat&logo=gmail&logoColor=white)

Lead Router Agent reads incoming sales inquiries, decides whether they're actually relevant to your business, figures out which team member should handle each one, and drafts an internal notification email — so leads stop landing in a shared inbox where nobody's sure who owns them.

## Why it exists

A lot of inbound leads are either irrelevant (job applications, spam, off-topic requests) or relevant but ambiguous about who should pick them up. Someone ends up manually reading every inquiry and forwarding it. Lead Router Agent automates that triage step: it reads the inquiry against your actual products/services and your team's areas of responsibility, and routes it — or discards it — accordingly.

## Features

### Relevance filtering
- Every lead is checked against your company's products and services. Job applications, spam, and unrelated requests are flagged invalid and never routed to anyone.

### Smart routing
- A configurable team directory (name, email, area of responsibility) lets the AI match each valid lead to the right person — not just the first person in a list.

### Review before it sends
- Every routed lead shows the AI's reasoning, the chosen recipient, and the drafted notification email. Nothing is sent until you click "Send notification" — no silent automation.

### Bring your own intake
- Submit leads manually from the dashboard, or wire your own website's contact form / CRM webhook to the API (documented below).

## How it works

```
A new lead comes in (manual entry or your own webhook)
                │
   AI checks it against your products & services
                │
        Invalid → flagged, nothing sent
                │
        Valid → AI matches it to the right team member
                │
      A notification email is drafted, not sent
                │
       You review it, then click "Send notification"
```

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Database | SQLite (local), PostgreSQL (production) |
| Email | Gmail API (OAuth 2.0, send-only scope) |
| AI | OpenAI-compatible SDK (swappable between OpenAI, Gemini, Groq) |
| Frontend | React, Vite, JavaScript, CSS |
| Hosting | Render (backend + PostgreSQL), Vercel (frontend) |

## Run locally

### Backend

```bash
cd backend
python -m venv venv
./venv/Scripts/activate   # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8070
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Setup

1. Set your company name and a description of your products/services on the Company page.
2. Add your team directory on the Team page — name, email, and what each person handles.
3. Get an LLM key (`LLM_API_KEY`, `LLM_MODEL`, `LLM_BASE_URL`) — see `.env.example` for free options (Gemini, Groq).
4. Create a Google Cloud project at [console.cloud.google.com](https://console.cloud.google.com), enable the **Gmail API**, and create an OAuth 2.0 Client ID (Web application). Add your `GOOGLE_REDIRECT_URI` as an authorized redirect URI. Free — no billing required for this scope.
5. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` in `backend/.env`.
6. Open the app, click **Connect Google**, and authorize.

To wire in real leads from your own site, `POST` to `/api/leads` with `{lead_name, company_name, notes, city, country, mobile, source}` — same shape the manual form uses.

Each user connects their own Google account and brings their own LLM key — nothing shared, nothing public.

## What's next

- Multiple recipients per lead with individual approve/decline.
- A public-facing intake form you can embed directly on your website.
- Slack or WhatsApp as an alternative notification channel.

## What Lead Router Agent will not do

- Will not notify anyone without you clicking "Send notification" first.
- Will not contact the lead directly — it only notifies your own team internally.
- Will not fabricate a recipient — if no team member is configured, nothing gets routed.
