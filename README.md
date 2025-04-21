<!--
SPDX-FileCopyrightText: 2024 Hitesh Arora
SPDX-FileContributor: Hitesh Arora

SPDX-License-Identifier: MIT
-->

<div align="center" markdown="1">
  <br />
  <h1>Stacked PR FastAPI Task Tracker</h1>
  <p>
    A clean, professional-grade backend project built with FastAPI, Docker, PostgreSQL, and SQLAlchemy.
  </p>
  <p>
    Built in a stacked PR workflow, step-by-step, from in-memory to production-ready DB logic.
  </p>

  <a href="#stacked-prs">Stacked PR Structure</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#usage">Usage</a> •
  <a href="#api">API</a> •
  <a href="#makefile">Makefile</a>

  <br />
  <br />

</div>

---

## 🌟 Stacked PRs

This repo is structured into clearly defined Pull Requests:

1. **`feat: add Task schema and in-memory task endpoints`**
2. **`feat: integrate PostgreSQL with SQLAlchemy and Alembic`**
3. **`feat: replace in-memory task store with PostgreSQL CRUD`**

Each PR builds cleanly on top of the previous, keeping history modular and understandable.

---

## 🚀 Tech Stack

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for PostgreSQL
- **Alembic**: Schema migrations
- **Docker + Compose**: Containerized dev environment
- **PostgreSQL**: Relational database
- **Pytest** (coming soon): Testing framework

---

## 📃 Project Structure

```bash
stacking_pr/
├── app/
│   ├── api/              # Routers
│   ├── db.py             # DB engine/session
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── dependencies.py   # FastAPI dependencies
├── alembic/              # Alembic migrations
├── alembic.ini           # Alembic config
├── Dockerfile            # FastAPI app container
├── docker-compose.yml    # Docker Compose setup
├── requirements.txt      # Python dependencies
├── Makefile              # Developer helper commands
└── README.md             # You're reading this
```

---

## 🚧 Usage

### ⚡ Run Locally

```bash
git clone https://github.com/yourname/stacking_pr.git
cd stacking_pr

# Build and run containers
make docker

# Run alembic migrations
make migrate

# Follow logs
make logs
```

Open browser:
```
http://localhost:8000/docs
```

To stop:
```bash
make docker-down
```

---

## 📊 API

### Create a Task
```http
POST /tasks
Content-Type: application/json

{
  "id": 1,
  "title": "Stacked PRs FTW!",
  "is_completed": false
}
```

### Get All Tasks
```http
GET /tasks
```

---

## 📄 Makefile

This project comes with a handy Makefile for development:

```makefile
make setup         # Create virtual environment and install dependencies
make install       # Install requirements into venv
make docker        # Start Docker containers
make docker-down   # Stop and remove containers
make migrate       # Run alembic migrations
make logs          # Follow Docker logs
make clean         # Delete venv + __pycache__
make test          # Run pytest tests (coming soon)
```

---

## ✅ License

This project is licensed under the MIT License.

---

## 🚀 Coming Soon

- 🌐 Deployment on Render/Railway
- ✅ Unit tests with Pytest
- 📊 GitHub Actions CI
- 👁️ Optional frontend in React or HTML

---

Made with ❤️ by Hitesh Arora.
