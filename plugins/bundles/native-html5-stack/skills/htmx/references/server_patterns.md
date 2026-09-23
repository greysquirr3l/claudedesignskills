# Server Patterns for HTMX

HTMX's server contract is small: any HTTP endpoint that returns an
HTML fragment is the only requirement. This reference shows idiomatic
implementations across the most common frameworks.

## The contract

1. **Detect HTMX requests** by checking `HX-Request: true` header
   (sent on every HTMX-issued request).
2. **For partial swaps**, return the partial template (no
   `<html>` / `<head>` / `<body>`).
3. **For OOB swaps**, include any number of fragments with
   `hx-swap-oob` attributes.
4. **For redirects**, set `HX-Redirect: <url>` header instead of
   returning 302.
5. **For trigger events**, set `HX-Trigger: <event-name>` (or
   `HX-Trigger-After-Swap` / `HX-Trigger-After-Settle`).
6. **For partial pushes**, set `HX-Push-Url: <url>` (htmx also
   pushes the URL when `hx-push-url="true"`).
7. **For 422 form validation**, return the re-rendered form
   (`hx-swap="innerHTML"` will replace the form with itself, errors
   included).

## Python — Flask

```python
@app.route("/search")
def search():
    if not request.headers.get("HX-Request"):
        return render_template("search.html")  # full page on direct hit
    q = request.args.get("q", "")
    results = Message.search(q)
    return render_template("partials/search.html", results=results)


@app.post("/messages")
def create_message():
    if not request.headers.get("HX-Request"):
        abort(400)
    form = MessageForm(request.form)
    if not form.validate():
        return render_template("partials/message_form.html", form=form), 422
    msg = form.save()
    resp = make_response(render_template("partials/message.html", m=msg))
    # Trigger a refresh of the count badge
    resp.headers["HX-Trigger"] = "messageCreated"
    return resp
```

## Python — Django

```python
from django.http import HttpResponse
from django.template.loader import render_to_string

def search(request):
    q = request.GET.get("q", "")
    results = Message.search(q)
    if request.headers.get("HX-Request") == "true":
        return HttpResponse(render_to_string("partials/search.html", {"results": results}))
    return render(request, "search.html", {"results": results})
```

## Node — Express (with Nunjucks)

```javascript
const router = require('express').Router()

router.get('/search', (req, res) => {
  const results = db.search(req.query.q)
  if (req.headers['hx-request']) {
    res.render('partials/search', { results })
  } else {
    res.render('search', { results })
  }
})

router.post('/messages', (req, res) => {
  try {
    const msg = db.create(req.body)
    res.render('partials/message', { msg }, (err, html) => {
      res
        .set('HX-Trigger', 'messageCreated')
        .send(html)
    })
  } catch (err) {
    res.status(422).render('partials/message-form', { error: err })
  }
})
```

## Go — net/http + html/template

```go
func search(w http.ResponseWriter, r *http.Request) {
    q := r.URL.Query().Get("q")
    results := db.Search(q)
    if r.Header.Get("HX-Request") == "true" {
        tmpl := template.Must(template.ParseFiles("templates/partials/search.html"))
        tmpl.Execute(w, results)
        return
    }
    tmpl := template.Must(template.ParseFiles("templates/search.html"))
    tmpl.Execute(w, results)
}

func createMessage(w http.ResponseWriter, r *http.Request) {
    msg, err := db.Create(r)
    if err != nil {
        w.WriteHeader(http.StatusUnprocessableEntity)
        tmpl := template.Must(template.ParseFiles("templates/partials/message-form.html"))
        tmpl.Execute(w, err)
        return
    }
    w.Header().Set("HX-Trigger", "messageCreated")
    tmpl := template.Must(template.ParseFiles("templates/partials/message.html"))
    tmpl.Execute(w, msg)
}
```

## Go — chi + templ

[templ](https://templ.guide) generates strongly-typed Go components
that compile to HTML. The contract is the same.

```templ
// messages.templ
package messages

templ Show(msg Message) {
    <li id={"message-" + msg.ID}>
        <span>{ msg.Body }</span>
        <button hx-delete={ "/messages/" + msg.ID }
                hx-confirm="Delete?"
                hx-target={"#message-" + msg.ID}
                hx-swap="outerHTML">×</button>
    </li>
}

templ Form(m Message, err error) {
    <form hx-post="/messages" hx-target="#status" hx-swap="innerHTML">
        <input name="body" value={ m.Body }>
        if err != nil {
            <p style="color:#dc2626">{ err.Error() }</p>
        }
        <button>Post</button>
    </form>
}
```

## Rust — Axum + askama

```rust
use askama::Template;
use axum::{extract::Form, http::HeaderMap, response::IntoResponse};

#[derive(Template)]
#[template(path = "partials/message.html")]
struct MessagePartial<'a> { msg: &'a Message }

async fn create(Form(input): Form<MessageInput>) -> impl IntoResponse {
    match db.create(input).await {
        Ok(msg) => {
            let html = MessagePartial { msg: &msg }.render().unwrap();
            let mut headers = HeaderMap::new();
            headers.insert("HX-Trigger", "messageCreated".parse().unwrap());
            (axum::http::StatusCode::OK, headers, html).into_response()
        }
        Err(err) => {
            let html = MessageFormPartial { err: &err }.render().unwrap();
            (axum::http::StatusCode::UNPROCESSABLE_ENTITY, html).into_response()
        }
    }
}
```

## Edge / Workers — Hono

Hono is the most idiomatic at-the-edge choice; perfect for Cloudflare,
Deno, and Bun:

```typescript
import { Hono } from 'hono'

const app = new Hono()

app.get('/search', async (c) => {
  const q = c.req.query('q') ?? ''
  const results = await db.search(q)
  if (c.req.header('HX-Request') === 'true') {
    return c.html(resultsPartial(results))
  }
  return c.html(searchPage(results))
})

app.post('/messages', async (c) => {
  const body = await c.req.parseBody()
  try {
    const msg = await db.create(body)
    c.header('HX-Trigger', 'messageCreated')
    return c.html(messagePartial(msg))
  } catch (err) {
    c.status(422)
    return c.html(messageFormPartial(body, err))
  }
})
```

## Static — Eleventy

```liquid
{% set q = "search" %}
{% if headers["HX-Request"] %}
  {% include "partials/search.html" %}
{% else %}
  {% include "search.html" %}
{% endif %}
```

Eleventy's passthrough-then-process flow isn't ideal for HTMX; consider
running both Eleventy and a small server-rendered route table.

## Static — Astro

```astro
---
// pages/api/search.astro
const q = Astro.url.searchParams.get('q')
const results = await db.search(q)
const isHtmx = Astro.request.headers.get('HX-Request') === 'true'
---
{isHtmx
  ? <Partial name="results">{results.map(Row)}</Partial>
  : <Layout title="Search">{results.map(Row)}</Layout>
}
```

## Content negotiation cheat-sheet

| HTMX wants… | Server should… |
|---|---|
| `<a hx-get="/">` | Return fragment matching `hx-target` |
| `<form hx-post="/">` | Return fragment with validation errors on 422 |
| Boosted `<a href="/">` | Return full document if non-HTMX request |
| `HX-Trigger` in response | `setHeader('HX-Trigger', 'event')` |
| Redirect after action | `setHeader('HX-Redirect', '/new-url')` |
| OOB swap | Include `<div id="x" hx-swap-oob="…">` anywhere in response |
| `HX-Boosted: true` | Boost-aware header in 2.x; htmx always sets `HX-Request` |

## Asset / response caching

- Dynamic fragments: `Cache-Control: private, max-age=0, no-store`.
- Public, cacheable fragments: set `Last-Modified` / `ETag` and let
  htmx send `If-None-Match` automatically.
- `Vary: HX-Request` is **NOT** correct — `HX-Request` is true for
  every HTMX-driven request, so it's a constant. The HTTP `Vary`
  header should be `Accept-Encoding`, `Accept`, etc.
