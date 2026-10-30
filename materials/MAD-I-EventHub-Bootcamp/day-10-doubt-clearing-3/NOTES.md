# Day 10 – Doubt clearing 3: final clinic + mock viva

**Goal:** every student leaves with a submission-ready project and has answered viva questions out loud at least once.

No new topics today. The reference code is `day-09-testing-and-submission/eventhub` (the finished project).

---

## Before the session

- Doubts in the shared form **by 12:00 noon**.
- Students bring: the running app, the report draft, the practice video link.

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:45 | Report and video questions; common last-minute bugs |
| 0:45 – 1:45 | Mock vivas in breakout rooms, about 5 minutes per student: 3 questions + 1 live change |
| 1:45 – 2:00 | Walk through the submission checklist together |

---

## Mock viva question bank

Ask 3 questions (one from each group) and one live change. Students answer about *their* project.

**How it works**

1. Walk me through what happens when a user submits the login form.
2. What does `create_app()` do, and why use a factory?
3. Where is the database created? Why must it be created by code?
4. What is the difference between `GET` and `POST`? Where do you use each?
5. Why do you redirect after a successful form submission?
6. What does `url_for` give you that a hard-coded URL does not?
7. How does a template get its data? What does `{% extends %}` do?

**Data and design**

8. Explain one relationship in your ER diagram and how SQLAlchemy represents it.
9. What happens to child rows when you delete a parent? Where is that decided?
10. Is any value in your app calculated instead of stored? Why?
11. How does your search work? Is it safe from SQL injection? Why?

**Security and APIs**

12. How are passwords stored? Why not store them directly?
13. How do you stop a normal user from opening an admin page?
14. What stops a user from cancelling or editing someone else's data?
15. Call one API endpoint and explain the status code it returns.
16. What happens if JavaScript is turned off in the browser?

**Live change (pick one)**

- Add a new field to a form and save it.
- Add a filter to a list page (e.g. only upcoming, or by city).
- Add a validation rule and show the error message.
- Change what a chart shows.

## Submission checklist

**App**

- [ ] Every core feature in the project statement works, for both roles
- [ ] Database is created by code on first run; no hand-made `.db` file is needed
- [ ] Admin is seeded by code; there is no admin registration
- [ ] Passwords are hashed; no secrets hard-coded in committed files
- [ ] Admin-only routes are blocked for normal users
- [ ] Forms validate input on the server
- [ ] Only the frameworks and libraries the project statement allows are used

**Repository and files**

- [ ] `requirements.txt` lists everything; the app runs from a fresh clone using the README alone
- [ ] `.gitignore` excludes `.venv`, `__pycache__` and the database file
- [ ] Regular commits across the bootcamp, not one final commit
- [ ] Zip and folder naming follow the submission instructions

**Report and video**

- [ ] Report has every section the project statement asks for
- [ ] Video within the time limit, shows every core feature, link access set correctly

**Viva readiness**

- [ ] Can explain any file and any line of your own code
- [ ] Can make a small change live

## Common mistakes

- Building the database manually in DB Browser instead of by code
- Checking roles only in templates (hiding a button) instead of in routes
- Adding a JavaScript framework the course does not allow for MAD I
- Leaving `debug=True` and a weak secret key without understanding them
- Copying code you cannot explain in the viva
