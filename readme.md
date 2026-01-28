## Configure
Environment is loaded from `.env`.

Example `.env` (local run):
```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/app
```

When running via Docker Compose, the DB host is `db` (not `localhost`). Compose already sets this for the app service.

## Run with Docker Compose
```bash
docker compose up --build
```

API:
- `http://localhost:8000`

pgAdmin:
- `http://localhost:5050`
- Email: `admin@admin.com`
- Password: `admin`

To connect pgAdmin to Postgres:
- Host: `db`
- Port: `5432`
- Database: `app`
- Username: `postgres`
- Password: `postgres`

## Run locally with Uvicorn
```bash
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API:
- `http://localhost:8000`

## Endpoints
- `PATCH /machines/{machine_id}/status` – machine status update (Guard/Domino/Log rules)


