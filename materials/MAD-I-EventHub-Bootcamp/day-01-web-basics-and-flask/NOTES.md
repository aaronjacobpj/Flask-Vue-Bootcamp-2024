# Day 1 – How the web works + first Flask app

**Goal:** every student has a running Flask app with a few routes, in their own Git repo.

**By the end, students can**
- explain what happens between typing a URL and seeing a page (client, server, request, response)
- read a request in browser DevTools: method, URL, status code, headers
- create a virtual environment, install Flask and write routes with path variables and query strings

BSCS2003 weeks covered: 1 (basic terminologies of the web).

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:15 | Bootcamp overview: show the finished EventHub (Day 9 code), the 10-day plan, the project statement |
| 0:15 – 0:35 | How the web works: client/server, HTTP request and response, methods, status codes, URLs (whiteboard) |
| 0:35 – 0:45 | DevTools demo: open any site, Network tab, read one request |
| 0:45 – 1:15 | Live code: venv, `pip install flask`, `app.py` with 4 routes |
| 1:15 – 1:50 | Hands-on: students create their project repo and a 3-route app |
| 1:50 – 2:00 | Recap, homework |

---

## Concepts in plain words

- **Client and server** – the browser (client) *asks*; the server *answers*. Every click or form submit is one request and one response.
- **HTTP request** – a method (`GET` = read, `POST` = send data), a path (`/hello/Priya`), optional query string (`?times=3`), headers.
- **HTTP response** – a status code (`200 OK`, `302 redirect`, `404 not found`, `500 server error`), headers and a body (HTML, JSON …).
- **Flask** – a small Python library that turns a URL into a function call. `@app.route("/about")` means "when someone requests `/about`, run this function and send back what it returns".
- **Path variable vs query string** – `/hello/<name>` is part of the path and identifies a thing; `?times=3` is an optional setting read with `request.args`.
- **Virtual environment** – a private folder of packages for one project, so projects don't break each other.
- **`debug=True`** – reloads on save and shows a detailed error page. Useful while coding; never in production.

---

## Live-coding script

| # | Do | Say / show |
|---|---|---|
| 1 | `mkdir eventhub && cd eventhub && git init` | One folder per project, under Git from minute one |
| 2 | `python -m venv .venv` then activate | Prompt changes to `(.venv)` – check this whenever something "isn't installed" |
| 3 | `pip install flask` then `pip freeze > requirements.txt` | `requirements.txt` lets anyone reinstall the same packages |
| 4 | Write `/` returning an HTML string, run `python app.py` | Point out the terminal log line: method, path, status |
| 5 | Add `/about` | A route is just a decorated function |
| 6 | Add `/hello/<name>` | Try `/hello/Priya`, `/hello/Rahul` – one function, many URLs |
| 7 | Add `?times=3` with `request.args.get(..., type=int)` | Try `?times=abc` – `type=int` falls back to the default |
| 8 | Add `/request-info` returning a dict | Flask turns a dict into JSON. Compare with what DevTools shows |
| 9 | Visit `/nope` | A 404 – Flask did it for us |
| 10 | Create `.gitignore`, commit, push to a **private** GitHub repo | Never commit `.venv/` or the database |

---

## Run & check

```bash
cd eventhub
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                      # http://127.0.0.1:5000
```

- `/` shows links; `/hello/Aaron?times=3` prints 3 lines; `/request-info` shows JSON.

## Common errors

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | venv not activated, or Flask installed in another Python |
| `python` not found (Windows) | use `py` instead of `python`, or reinstall Python with "Add to PATH" ticked |
| `Address already in use` / port 5000 busy | another app is running; stop it, or `app.run(debug=True, port=5001)`. On macOS, turn off AirPlay Receiver |
| Changes not showing | `debug=True` missing, or the server was started from another folder |
| PowerShell blocks `activate` | run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once |

## Homework

1. Read the project statement end to end. List every **role** and every **feature** it asks for (a simple table).
2. Add two more routes to your app and push to GitHub.
3. Open DevTools on three websites and note one status code other than 200.
