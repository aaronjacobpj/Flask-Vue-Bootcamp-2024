# Project report template (MAD I)

Follow your term's project statement for page limits, format (usually PDF) and required sections. This template covers what reports usually need. Keep it short, specific and true to your code.

---

## 1. Student details

Name · Roll number · Student email · One line about yourself (optional)

## 2. Project details

- **Problem statement** – the project title and what the app does, in 2–3 sentences, in your own words.
- **Approach** – how you went about it: the order you built it in and the key decisions (for example: "seats left is calculated from bookings, not stored").

## 3. Frameworks and libraries used

| Library | Used for |
|---|---|
| Flask | routing, request handling |
| Flask-SQLAlchemy | models and queries |
| Flask-Login | sessions, login_required |
| Flask-RESTful | API resources |
| Jinja2, Bootstrap 5 | templates and styling |
| Chart.js | summary charts |
| pytest | automated tests |

## 4. ER diagram

Insert the diagram. Under it, one line per relationship, e.g. "A venue has many events; deleting a venue deletes its events."

## 5. API resource endpoints

| Method | URL | Who | Purpose |
|---|---|---|---|
| GET | `/api/venues` | anyone | list venues |
| … | … | … | … |

Mention how you tested them (Postman collection or curl commands).

## 6. Features

Core features (as listed in the project statement) and any additional features, each in one line. Mark which role uses each.

## 7. Use of AI / LLM tools

If your term asks for it, state honestly which tools you used, for what, and roughly how much of the work they did.

## 8. Video link

The drive link to the presentation video, with access set as the instructions require.
