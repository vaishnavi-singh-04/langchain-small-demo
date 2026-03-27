# LangChain RAG API

This is a FastAPI-based REST API for uploading documents and asking questions using LangChain and RAG (Retrieval-Augmented Generation).

## Prerequisites
- Python 3.10+ (Recommended)
- PostgreSQL (or your configured database for Alembic and pgvector)

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Linux/macOS:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment variables in the `.env` file (e.g., database connection strings, API keys).

## Database Migrations (Alembic)

This project uses Alembic to handle database schema changes. Below are all the commands required for managing your migrations.

### Apply Migrations (Up)

To upgrade the database to the latest migration revision:
```bash
alembic upgrade head
```
*(You can also upgrade to a specific revision by replacing `head` with the revision ID)*

### Revert Migrations (Down)

To revert the most recent migration:
```bash
alembic downgrade -1
```
*(To completely revert all migrations to the initial state, use `alembic downgrade base`)*

### Create a New Migration

After modifying your SQLAlchemy models, generate a new migration script by running:
```bash
alembic revision --autogenerate -m "Description of your changes"
```

### View Migration History
To see the history of all migrations:
```bash
alembic history --verbose
```

### Check Current Revision
To find out which version your database is currently on:
```bash
alembic current
```

## Running the Application

To run the FastAPI server, use the `uvicorn` command:

```bash
uvicorn main:app --reload
```

- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative API Docs (ReDoc)**: `http://127.0.0.1:8000/redoc`
