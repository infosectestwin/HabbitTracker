# Security Policy

## Current Security Implementation

### 1. Authentication & Authorization
- **Flask-Login:** Managed sessions for authenticated users.
- **Password Hashing:** Uses `werkzeug.security` (PBKDF2 with SHA-256) for secure password storage.
- **Password Complexity:** Enforced 8+ characters with uppercase, lowercase, numbers, and special characters.
- **Access Control:** `@login_required` decorators on all protected routes; habit ownership is verified before modification.

### 2. Logging & Monitoring
- **Structured JSON Logging:** Centralized logging via `app/logging_config.py`.
- **Request Metadata:** Automatically logs HTTP method, path, status code, duration, client IP, and `user_id`.
- **Audit Trail:** Habit completions and modifications are logged via `HabitLog`.

### 3. HTTP Security Headers
The following headers are automatically added to all responses in `app/__init__.py`:
- **Content-Security-Policy (CSP):** Restricts script/style sources; includes a `nonce` for inline content.
- **X-Content-Type-Options:** Set to `nosniff` to prevent MIME-sniffing.
- **X-Frame-Options:** Set to `DENY` to prevent clickjacking.
- **Referrer-Policy:** Set to `strict-origin-when-cross-origin`.
- **HSTS:** Enabled for HTTPS connections to enforce encryption.

---

## Remaining Risks & Mitigation

| Risk | Description | Mitigation Plan |
| :--- | :--- | :--- |
| **CSRF** | Cross-Site Request Forgery on habit actions. | Enable `Flask-WTF` CSRF protection on all POST routes. |
| **Rate Limiting** | Potential for brute-force attacks on login/register. | Implement `Flask-Limiter` on authentication routes. |
| **Session Fixation** | Session IDs might persist after login. | Ensure `session.regenerate()` is called on login. |
| **Database Exposure** | SQLite file is stored locally in `instance/`. | Ensure the `instance/` folder is never committed and has strict OS permissions. |
| **Third-Party CDNs** | CSP allows scripts from `unpkg.com` and `tailwindcss.com`. | Consider bundling dependencies locally to remove external script dependencies. |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please do not open a public issue. Instead, contact the maintainers directly.
