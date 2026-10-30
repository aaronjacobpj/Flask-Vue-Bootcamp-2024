# Day 2 – HTML, CSS, Bootstrap + Jinja2 views

**Goal:** EventHub has a shared layout and four real-looking pages, rendered by Flask with Jinja2.

**By the end, students can**
- write semantic HTML with forms and the right input types
- lay out a responsive page with the Bootstrap grid, navbar, cards and tables
- use Jinja2: variables, `for` / `if`, template inheritance (`extends` / `block`), `url_for`, static files

BSCS2003 weeks covered: 2 (HTML and CSS), 3 (presentation layer: view).

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:15 | Recap Day 1, check every student has a running app |
| 0:15 – 0:35 | HTML structure, forms and input types; CSS box model; what Bootstrap gives us |
| 0:35 – 1:15 | Live code: `templates/`, `base.html`, `index.html` with a loop, login/register/admin pages |
| 1:15 – 1:50 | Hands-on: students build their base layout + 4 static pages |
| 1:50 – 2:00 | Recap, homework |

---

## Concepts in plain words

- **Template** – an HTML file with holes. `render_template("index.html", events=EVENTS)` fills the holes with Python data.
- **Jinja2 syntax** – `{{ value }}` prints; `{% for %}` / `{% if %}` control; `{# comment #}` is hidden from the browser.
- **Template inheritance** – `base.html` holds the navbar and footer once. Every page says `{% extends "base.html" %}` and fills `{% block content %}`. Change the navbar in one place.
- **`url_for("login")`** – builds the URL from the *function name*. If the URL changes later, links still work.
- **Static files** – CSS, JS and images live in `static/`; link them with `url_for('static', filename='css/style.css')`.
- **Auto-escaping** – Jinja escapes `<` and `>` in `{{ }}`, so a user typing `<script>` cannot inject code.
- **Bootstrap grid** – a row has 12 columns. `col-12 col-md-6 col-lg-4` = full width on phones, half on tablets, a third on laptops.

---

## Live-coding script

| # | Do | Say / show |
|---|---|---|
| 1 | Create `templates/` and `static/css/` | Flask looks in these folders by name |
| 2 | Write `base.html`: Bootstrap CDN link, navbar, `{% block content %}` | Copy the Bootstrap starter template, then trim it |
| 3 | Add the `EVENTS` list in `app.py`; write `index.html` with `{% for event in events %}` cards | Data comes from Python; the template only displays it |
| 4 | Add `{% if event.price == 0 %}Free{% endif %}` and the sold-out badge | Logic for *display* belongs in the template; business logic does not |
| 5 | Add `{% else %}` to the `for` loop | Shows "No events yet" when the list is empty – empty `EVENTS = []` to prove it |
| 6 | Write `auth/login.html` and `auth/register.html` forms | `type="email"`, `required`, `minlength` – free validation in the browser |
| 7 | Write `admin/dashboard.html` with a table and `loop.index` | `table-responsive` makes tables scroll on phones |
| 8 | Replace hard-coded links with `url_for(...)` | Rename a route to show why |
| 9 | Resize the browser / DevTools phone view | The navbar collapses, cards stack |

---

## Run & check

```bash
cd eventhub
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

- `/` shows 3 event cards (one free, one sold out). `/login`, `/register`, `/admin` all share the navbar.
- The forms show but do not submit yet (they work on Day 6).

## Common errors

| Error | Fix |
|---|---|
| `TemplateNotFound: index.html` | the folder must be called `templates` (plural), next to `app.py` |
| `BuildError: Could not build url for endpoint 'home'` | `url_for` takes the **function name**, not the URL or the file name |
| CSS file not loading (404 in DevTools) | folder must be `static/`; check the `filename=` path |
| Page looks unstyled | Bootstrap `<link>` missing, or no internet for the CDN |
| `jinja2.exceptions.TemplateSyntaxError` | a `{% for %}` or `{% if %}` without its `{% endfor %}` / `{% endif %}` |

## Homework

1. Sketch a wireframe (paper is fine) for **every page** your project needs, for both roles.
2. Convert two of your wireframes into static templates.
3. Read the Jinja "Template Designer Documentation" sections on loops and inheritance.
