# Spec: Registration

## Overview

Implements the working `POST /register` flow: a visitor fills in the existing registration form and a real user row is created in SQLite with a securely hashed password. Step 1 built the `users` table and the `database/db.py` helpers (`get_db`, `init_db`, `seed_db`); this step is the first feature to actually write a new user into that table through the app itself, rather than through the seed data. Login (`POST /login`) and session handling are explicitly out of scope for this step — after a successful registration the user is redirected to `/login` to sign in.

## Depends on

- Step 1 (Database setup) — requires the `users` table, `get_db()`, and `init_db()` from `database/db.py`.

## Routes

- `POST /register` — accepts the registration form (`name`, `email`, `password`), creates a new user, and redirects to `/login` on success or re-renders `register.html` with an error on failure — public

(`GET /register` already exists and is unchanged.)

## Database changes

No database changes. The existing `users` table (`id`, `name`, `email` UNIQUE NOT NULL, `password_hash` NOT NULL, `created_at`) already supports this feature — verified against `database/db.py`.

## Templates

**Create:** none — `templates/register.html` already exists.

**Modify:**
- `templates/register.html` — change `<form method="POST" action="/register">` to use `action="{{ url_for('register') }}"` instead of a hardcoded path.

## Files to change

- `app.py` — change the `register` route to accept `GET` and `POST`. On `POST`: read `name`, `email`, `password` from the form, call the new `database/db.py` helper to create the user, redirect to `url_for('login')` on success. On duplicate email (or other validation failure), re-render `register.html` with an `error` message and the submitted values.
- `database/db.py` — add:
  - `get_user_by_email(email)` — parameterized `SELECT` returning the matching user row or `None`.
  - `create_user(name, email, password)` — hashes `password` with `werkzeug.security.generate_password_hash` (mirroring the existing pattern in `seed_db`) and inserts the row via a parameterized `INSERT`.

## Files to create

None.

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with werkzeug (`generate_password_hash`), never stored in plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic (queries, hashing) stays in `database/db.py` — the route only reads form data, calls the helper, and renders/redirects
- Every internal link/form action uses `url_for()` — never a hardcoded path

## Definition of done

- [ ] Visiting `/register` still renders the form as before
- [ ] Submitting the form with a new name/email/password redirects to `/login`
- [ ] After that submission, the new user appears in the `users` table (check via `sqlite3 expense_tracker.db "SELECT name, email FROM users;"`) with a `password_hash` that is **not** the plaintext password
- [ ] Submitting the form again with the same email shows an error on the `register.html` page (no 500, no crash) instead of a raw SQLite `IntegrityError`
- [ ] Submitting with an empty `name`, `email`, or `password` does not create a row (either blocked by the browser's `required` attributes or rejected server-side)
- [ ] Viewing the page source of `/register` shows the form's `action` resolved via `url_for()`, not a hardcoded `/register` string
- [ ] `database/db.py` contains no string-formatted/f-string SQL — only `?` placeholders
