# student-ml-api

A minimal Flask inference API used to demonstrate a production-style MLOps
CI/CD workflow: feature branches, Pull Requests, GitHub Actions CI,
Dockerized builds, and versioned publishing to a container registry.

## Endpoints

| Method | Path       | Description                          |
|--------|------------|---------------------------------------|
| GET    | `/health`  | Liveness/readiness check              |
| POST   | `/predict` | Returns a prediction for `{"value": n}` |

## Local development

```bash
python -m venv .venv
.venv/Scripts/activate      # Windows
pip install -r requirements-dev.txt
pytest -v
python app.py                # serves on http://localhost:5000
```

## Workflow

Development happens on feature branches and reaches `main` only through
reviewed, CI-validated Pull Requests. See `.github/workflows/` for the CI
and release pipelines.
