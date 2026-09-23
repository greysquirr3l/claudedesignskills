# HTMX Security Checklist

HTMX is a thin layer over HTML, so most attacks are the same as any
HTML application — but a few HTMX-specific vectors deserve attention.

## Cross-Site Request Forgery (CSRF)

If your site has any user-controlled state, every state-changing
endpoint must enforce CSRF. With HTMX the form still submits to your
origin so traditional protections apply:

1. **Synchronizer token** — render an `<input type="hidden"
   name="csrf_token" value="…">` in every form, validate server-side.
2. **Header-bound token** — easier with HTMX; read the cookie value
   `htmx.config.csrfToken` and add it as `X-CSRF-Token` on every
   request:

   ```javascript
   document.body.addEventListener('htmx:configRequest', (e) => {
     const tok = document.cookie.match(/csrf=([^;]+)/)?.[1]
     if (tok) e.detail.headers['X-CSRF-Token'] = tok
   })
   ```

3. **SameSite cookies** — ship the session cookie with
   `SameSite=Lax` (or `Strict` if you're not worried about
   cross-origin links).
4. **`htmx.config.selfRequestsOnly = true`** (default in 2.x) to
   refuse cross-origin requests.

## Cross-Site Scripting (XSS)

HTMX swaps **HTML** into the DOM. So the *server-side template* must
produce safe HTML:

1. Always escape dynamic values server-side (`{{ name }}` — never
   `{{{ name }}}`).
2. For WYSIWYG / markdown user input, sanitise on the server with a
   mature library (`bleach`, `sanitize-html`, `ammonia`,
   `markdown-it` + DOMPurify client-side after swap).
3. Set `htmx.config.allowScriptTags = false` so any rogue `<script>`
   in a response is stripped before the swap.

## DOM clobbering via `id` attributes

HTMX targets elements by `id`. If you let users pick `id` values,
they can hijack your `hx-target`:

1. Never let user-generated values become element IDs.
2. Use `hx-target="closest .card"` instead of `hx-target="#user-id"`
   whenever possible.

## HTTP method confusion

`<a hx-delete="/api/post/1">` is *unconventional* — `hx-delete` is
the right form:

1. CSRF protections differ between GET (low risk) and POST/PUT/DELETE
   (high risk). Always validate that dangerous operations require a
   valid CSRF token, regardless of the verb.

## History cache

`htmx.config.historyCacheSize = 20` bounds the in-memory history
cache. Sensitive routes should also send `Cache-Control: no-store` so
no browser or proxy layer caches the response.

## SSRF / abused endpoints

If your HTMX endpoints talk to internal services, validate
`HX-Request` server-side:

```python
if not request.headers.get("HX-Request"):
    abort(403)
```

Otherwise your JSON / API endpoints become a SSRF vector because the
same URL serves both narrative UI and JSON consumers. Either gate
them or namespace them (`/api/x` for JSON, `/hx/x` for fragment).

## CSP and HTMX

```http
Content-Security-Policy:
  default-src 'self';
  script-src  'self' https://cdn.jsdelivr.net 'unsafe-inline';
  style-src   'self' 'unsafe-inline';
  img-src     'self' data: https:;
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri    'self';
  form-action 'self';
```

- Don't `unsafe-eval` (htmx doesn't need it).
- Inline script sources are fine for htmx's `hx-on::` (which uses
  `Function()` only if you allow it — set `htmx.config.allowEval = false`).
- `frame-ancestors 'none'` defends against clickjacking.

## `hx-on::eval` / `hx-on::load`

`hx-on::eval` runs server-rendered JavaScript expressions — usually a
fingerprint attack vector. Set:

```javascript
htmx.config.allowEval = false
```

## Logging & privacy

`htmx:afterRequest` events include the URL and response status. Log
them; redact Authorization headers; redact query-string secrets (avoid
them altogether — `POST` with body or `HX-Trigger` header is safer).

## Network policies

- `htmx.config.timeout = 8000` (8 s) prevents silent hangs.
- Lock down `htmx.config.selfRequestsOnly = true` to refuse
  cross-origin traffic.

## Audit checklist (pass before shipping)

- [ ] CSRF enforced on every POST / PUT / PATCH / DELETE
- [ ] All HTML fragments escape dynamic values server-side
- [ ] User-rendered markdown / WYSIWYG sanitised
- [ ] `allowScriptTags = false` and `allowEval = false`
- [ ] `selfRequestsOnly = true`
- [ ] `timeout` configured
- [ ] `historyCacheSize` bounded
- [ ] CSP set, no `unsafe-eval`, no `unsafe-inline` on `script-src`
- [ ] Sensitive routes send `Cache-Control: no-store`
- [ ] `HX-Request` validated for endpoints that aren't HTMX-specific
- [ ] No secrets in URLs; use `HX-Trigger` header or POST body
- [ ] DOM IDs are not user-controlled
- [ ] Server endpoints distinguish HTMX (fragment) from non-HTMX (full
      document) via `HX-Request` header
