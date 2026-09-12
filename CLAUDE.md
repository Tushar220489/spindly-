# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

"Spendly" — a Flask-based personal expense tracker, built as a step-by-step learning scaffold. Routes and files carry `# Step N` comments marking a guided build sequence (DB setup, auth, expense CRUD). Most functionality is currently unimplemented stubs; treat comments like "Students will implement..." as the spec for what needs to be built, not as existing behavior.

## Commands

```bash
# Activate the virtualenv (already created at venv/)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dev server (http://localhost:5001, debug mode on)
python app.py

# Run tests
pytest

# Run a single test file / test
pytest path/to/test_file.py
pytest path/to/test_file.py::test_name
```

There is no build step, linter, or frontend tooling (no npm/webpack) — static assets in `static/` are served as-is by Flask.

## Architecture

- **Single-file Flask app** (`app.py`): all routes live here directly on the `app` object — no blueprints, no app-factory pattern, no `models.py`/`config.py`. New routes should follow this same flat style unless the project grows enough to warrant splitting it up.
- **Database layer** (`database/db.py`): currently an empty stub. It is meant to hold three functions per its header comment:
  - `get_db()` — returns a SQLite connection with `row_factory` and foreign keys enabled
  - `init_db()` — creates tables via `CREATE TABLE IF NOT EXISTS`
  - `seed_db()` — inserts sample dev data
  `database/` is a proper package (has `__init__.py`), so import as `from database.db import get_db`. No ORM is used — expect raw SQL via the stdlib `sqlite3` module. The resulting DB file is `expense_tracker.db` at the project root (already gitignored).
- **Templates** (`templates/`, Jinja2): `base.html` is the shared layout (navbar, footer, font/CSS includes) that all pages extend via `{% block content %}`. Auth pages (`login.html`, `register.html`) already post to `/login` and `/register` and render an `error` block, but `app.py` only has GET handlers for those routes so far — POST handling, session/auth logic, and password hashing still need to be added.
- **Static assets** (`static/`): `css/style.css` is a single stylesheet driven by CSS custom properties defined in `:root` (colors, fonts, spacing) — reuse these variables rather than hardcoding new values. `js/main.js` is an empty stub for future client-side behavior.
- **Placeholder routes**: `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` currently return plain strings ("coming in Step N") instead of real behavior — these are the main routes left to implement, and will depend on the database layer and auth/session state being built first.
