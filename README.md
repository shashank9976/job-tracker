# Job Application Tracker API

A FastAPI + SQLAlchemy + SQLite application for tracking target companies, outreach contacts, replies, follow-ups, and pipeline progress. It includes a vanilla JavaScript frontend served directly by the API.

## Local setup

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/ for the UI or http://127.0.0.1:8000/docs for Swagger documentation.

Run tests with:

```bash
pytest
```

## Docker setup

```bash
docker compose up --build
```

The SQLite database is stored in the `sqlite-data` Docker volume and persists across container restarts.

## API routes

| Endpoint | Method | Description |
|---|---:|---|
| `/companies` | POST | Create a company |
| `/companies` | GET | List companies with optional filters |
| `/companies/{id}` | GET | Get one company |
| `/companies/{id}` | PUT | Update a company |
| `/companies/{id}` | DELETE | Delete a company and its contacts |
| `/contacts` | POST | Create a contact |
| `/contacts` | GET | List contacts with optional filters |
| `/contacts/{id}` | GET | Get one contact |
| `/contacts/{id}` | PUT | Update a contact |
| `/contacts/{id}` | PATCH | Update only contact pipeline status |
| `/contacts/{id}` | DELETE | Delete a contact |
| `/contacts/{id}/days-since-sent` | GET | Calculate days since outreach |
| `/stats/summary` | GET | Return outreach and reply statistics |
| `/stats/by-tier` | GET | Return email totals grouped by tier |
| `/reminders` | GET | List contacts needing follow-up |
| `/reminders/digest` | POST | Return a plain-text follow-up digest |

## Roadmap

### Implemented

- Company and contact CRUD
- SQLite persistence and first-run seed data
- Outreach analytics and reply rate
- Follow-up reminders and digest payload
- Browser UI with dashboard, filters, modals, and drag-and-drop pipeline
- CORS, OpenAPI docs, pytest coverage, Docker, and GitHub Actions CI

### Planned

- Authentication and multi-user workspaces
- Email or Slack webhook delivery for reminder digests
- Scheduled reminder jobs
- CSV import/export
- Production database and deployment configuration
