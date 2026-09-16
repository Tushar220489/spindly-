# Spec: Profile Page

## Overview

Implements the real `GET /profile` route as the logged-in user's home page. Spendly's roadmap has no separate "dashboard" or "expenses list" route (only `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`, all still stubs), so `/profile` is where a signed-in user sees their account info and their expense history — it's also exactly where Step 3's `POST /login` already redirects on success. This step also introduces the app's first login-gated page: visiting `/profile` without a session must redirect to `/login` rather than expose the page.

## Depends on

- Step 1 (Database setup) — requires the `expenses` table and `get_db()`.
- Step 3 (Login and Logout) — requires `session["user_id"]` to identify the logged-in user; `/profile` is only reachable with a valid session.

## Routes

- `GET /profile` — if no `session["user_id"]`, redirect to `/login`; otherwise fetch the user's account info and their expenses, compute the total spent, and render `profile.html` — logged-in

## Database changes

No schema changes. The existing `users` table (`id`, `name`, `email`, ...) and `expenses` table (`id`, `user_id`, `amount`, `category`, `date`, `description`, ...) already support this feature — verified against `database/db.py`. Two new read-only helpers are needed:

- `get_user_by_id(user_id)` — parameterized `SELECT * FROM users WHERE id = ?`, mirrors the existing `get_user_by_email`.
- `get_expenses_by_user(user_id)` — parameterized `SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC`, returns all of that user's expense rows.

Total spent is computed in `app.py` by summing the amounts from `get_expenses_by_user`'s result — a one-line aggregation of already-fetched data, not a separate DB query.

## Templates

**Create:**
- `templates/profile.html` — extends `base.html`; shows the user's name and email, the total spent, and a list of their expenses (date, category, description, amount); includes an "Add Expense" link and, per expense, "Edit"/"Delete" links. These link to the existing `add_expense`/`edit_expense`/`delete_expense` routes via `url_for()` — those routes are still Step 7/8/9 stubs, so clicking them will show their placeholder text for now, which is expected and out of scope for this step.

**Modify:**
- `templates/base.html` — the nav currently shows only a "Logout" link when logged in (from Step 3). Add a "Profile" link next to it (`url_for('profile')`) so a logged-in user has a way back to their profile from anywhere in the site.

## Files to change

- `app.py` — replace the `profile` stub with a real route: check `session.get("user_id")`, redirect to `url_for('login')` if absent; otherwise call `get_user_by_id` and `get_expenses_by_user`, sum the expense amounts, and render `profile.html` with `user`, `expenses`, and `total_spent`. Move it out of the "Placeholder routes" comment block, per `CLAUDE.md`'s rule that a stub becomes real once its step lands.
- `database/db.py` — add `get_user_by_id(user_id)` and `get_expenses_by_user(user_id)`.
- `templates/base.html` — add the "Profile" nav link described above.

## Files to create

- `templates/profile.html`
- `static/css/profile.css` — page-specific styles for the profile layout and expense list (mirrors how `landing.css` is scoped to `landing.html` only), linked from `profile.html`'s `{% block head %}`. Uses the existing CSS variables (`--ink`, `--paper-card`, `--border`, `--accent`, `--radius-md`, etc.) — no hardcoded hex values.

## New dependencies

No new dependencies.

## Rules for implementation

- No SQLAlchemy or ORMs
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with werkzeug (unaffected by this step — no password handling here)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic (all queries) stays in `database/db.py` — the route only checks the session, calls the helpers, sums amounts, and renders
- Every internal link uses `url_for()` — never a hardcoded path
- Unauthenticated access to `/profile` must redirect, never render user data or error out

## Definition of done

- [ ] Visiting `/profile` while logged out redirects to `/login` (no data leaked, no 500)
- [ ] Logging in as the seeded demo user (`demo@spendly.com` / `demo123`) and visiting `/profile` shows the name "Demo User" and email `demo@spendly.com`
- [ ] The profile page lists all 8 seeded expenses with their correct category, date, description, and amount
- [ ] The total spent shown on the page equals the sum of the seeded expenses' amounts
- [ ] The nav bar shows both "Profile" and "Logout" links while logged in
- [ ] After `/logout`, visiting `/profile` again redirects to `/login` instead of showing stale data
- [ ] Viewing the page source of `/profile` shows every internal link/href resolved via `url_for()`, not a hardcoded path
- [ ] `database/db.py` contains no string-formatted/f-string SQL — only `?` placeholders
- [ ] `requirements.txt` is unchanged
