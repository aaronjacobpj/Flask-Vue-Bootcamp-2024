# Day 7 – Doubt clearing 2: mid-project code review and debugging

**Goal:** every student's core flows (both roles) work end to end before APIs and charts are added.

No new topics today. There is no code folder: the reference for today is `day-06-auth-and-security/eventhub`.

---

## Before the session

- Doubts in the shared form **by 12:00 noon**: repo link, the broken feature, the full traceback (copy the text from the terminal).
- Two or three students volunteer for a full screen-share code review.

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:20 | Live debugging of 2–3 submitted bugs, showing *how* to debug (below) |
| 0:20 – 1:40 | Screen-share code reviews, about 10 minutes each, using the review checklist |
| 1:40 – 2:00 | Q&A on the user-side flows; what must work before Day 8 |

---

## How to debug (show this live)

1. **Read the last line of the traceback first** – it names the error. Then find the first line that points into *your* files.
2. **Reproduce it** – which URL, which button, which input?
3. **Look at the data** – `print()` the variable, or open the DB in DB Browser.
4. **Use the debugger page** (`debug=True`) – the console icon on each frame lets you inspect variables.
5. **Check the request** – DevTools → Network: was it GET or POST? What form fields were sent? What status came back?
6. **Change one thing at a time**, then retest.

## Common bugs at this stage

| Symptom | Likely cause |
|---|---|
| `405 Method Not Allowed` | form posts to a route without `methods=["POST"]` |
| `400 Bad Request: KeyError` | `request.form["field"]` for a field the form does not send (check the input's `name=`) |
| Data saved but page shows old values | missing `db.session.commit()`, or the page was not reloaded from the database |
| `DetachedInstanceError` | using a model object after the session closed – query it inside the request |
| User sees another user's data | query not filtered by `current_user.id` |
| Admin pages open to users | `@admin_required` missing on some route |
| `UnboundLocalError` in a POST route | a variable is set only inside `if request.method == "POST"` but used after it |
| Counts or totals wrong after cancel/delete | totals stored in a column instead of calculated |
| `sqlite3.OperationalError: database is locked` | DB Browser has unsaved changes open – close it or click "Write Changes" |

## Code review checklist (10 minutes per student)

- [ ] Can you log in as admin and as a user, and does each see only their pages?
- [ ] Does every form validate on the server and keep the typed values on error?
- [ ] Are routes thin? (Long repeated logic → a helper function)
- [ ] Is there a redirect after every successful POST?
- [ ] Are deletes POST with a confirmation?
- [ ] Do URLs with ids check ownership?
- [ ] Are templates using `base.html` and `url_for` everywhere?
- [ ] Is the repo clean: `.gitignore`, `requirements.txt`, regular commits?

## Exit check

All core features of the project statement work for both roles, even if the UI is plain. APIs and charts come on Day 8.
