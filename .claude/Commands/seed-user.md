---
description: Add a new user to the Spendly database
argument-hint: [name] [email] [password]
---

Add a new user row to the `users` table in the Spendly SQLite database.

Arguments (`$ARGUMENTS`) may supply `name`, `email`, and `password` in that order,
space-separated. If any are missing or `$ARGUMENTS` is empty, ask the user for
whichever fields weren't provided before continuing.

Steps:
1. Import `get_db` from `database.db` (per CLAUDE.md: DB logic only ever goes
   through `database/db.py`, never inline elsewhere).
2. Hash the password with `werkzeug.security.generate_password_hash` — never
   store it in plaintext.
3. Insert the row using a parameterized query only:
   `INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)`.
   Never use string formatting/f-strings to build the SQL.
4. If the insert fails with a UNIQUE constraint violation on `email`, report
   clearly that the email is already registered — don't treat it as a crash.
5. On success, report the new user's `id`, `name`, and `email`.
