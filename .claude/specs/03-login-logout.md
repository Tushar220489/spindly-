# Spec: Login and Logout

## Overview

Implements the working `POST /login` flow and a real `GET /logout` route. Step 1 built the `users` table and `database/db.py` helpers; Step 2 made `POST /register` create real user rows. This step lets an existing user (registered or the seeded demo account) actually authenticate: submitting `login.html` verifies their email/password against the `users` table and starts a session, and `/logout` ends that session. Session-protected pages (e.g. a real `/profile`) are out of scope — this step only establishes the session itself and lets the nav reflect logged-in state.

## Depends on

- Step 1 (Database setup) — requires the `users` table and `get_db()` from `database/db.py`.
- Step 2 (Registration) — requires `create_user()`/real user rows to log in with (or the seeded demo user, `demo@spendly.com` / `demo123`).

## Routes

- `POST /login` — accepts the existing login form (`email`, `password`), verifies credentials, and on success stores the user in the session and redirects to `/profile`; on failure re-renders `login.html` with an error — public
- `GET /logout` — clears the session and redirects to `/` — logged-in (safe to call when already logged out; just no-ops)

(`GET /login` already exists and is unchanged.)

## Database changes

No database changes. The existing `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already supports this feature — verified against `database/db.py`. One new helper function is needed (see below), but no schema changes.

## Templates

**Create:** none.

**Modify:**
- `templates/login.html` — change `<form method="POST" action="/login">` to `action="{{ url_for('login') }}"`.
- `templates/base.html` — nav currently always shows "Sign in" / "Get started". Make it session-aware: when a user is logged in, show a "Logout" link (`url_for('logout')`) instead; keep "Sign in" / "Get started" for logged-out visitors.

## Files to change

- `app.py`:
  - Set `app.secret_key` (required for Flask's session to work; none is configured today).
  - Change the `login` route to accept `GET` and `POST`. On `POST`: read `email`/`password` from the form, call the new `database/db.py` helper to authenticate, store `session["user_id"]` (and `session["user_name"]`) on success and redirect to `url_for('profile')`; on failure re-render `login.html` with an `error` message.
  - Implement `logout`: clear the session (`session.clear()`) and redirect to `url_for('landing')`.
- `database/db.py` — add `authenticate_user(email, password)`: parameterized `SELECT` by email (reuses the same lookup as `get_user_by_email`), then `werkzeug.security.check_password_hash` against the stored hash; returns the user row on match, `None` otherwise.

## Files to create

None.

## New dependencies

No new dependencies. Flask's session support is built in; `check_password_hash` is already imported via `werkzeug.security` (mirrors `generate_password_hash` used in Step 2).

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — no f-strings in SQL
- Passwords verified with werkzeug (`check_password_hash`) — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic (queries, password verification) stays in `database/db.py` — the route only reads form data, calls the helper, and manages the session/redirect
- Every internal link/form action uses `url_for()` — never a hardcoded path

## Definition of done

- [ ] Visiting `/login` still renders the form as before
- [ ] Logging in with the seeded demo account (`demo@spendly.com` / `demo123`) redirects to `/profile`
- [ ] Logging in with a correct email but wrong password re-renders `login.html` with an error (no 500, no crash)
- [ ] Logging in with an email that doesn't exist re-renders `login.html` with an error (no 500, no crash)
- [ ] After a successful login, visiting `/logout` clears the session and redirects to `/`
- [ ] After `/logout`, the nav bar shows "Sign in" / "Get started" again (not the logged-in state)
- [ ] While logged in, the nav bar shows a "Logout" link instead of "Sign in" / "Get started"
- [ ] Viewing the page source of `/login` shows the form's `action` resolved via `url_for()`, not a hardcoded `/login` string
- [ ] `database/db.py` contains no string-formatted/f-string SQL — only `?` placeholders
- [ ] `requirements.txt` is unchanged
