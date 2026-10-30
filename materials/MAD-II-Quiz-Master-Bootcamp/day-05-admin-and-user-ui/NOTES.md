# Day 5 – Admin & user screens

**Goal:** the complete UI. The admin manages all content and users; users take timed quizzes and see their scores.

**By the end, students can**
- build CRUD screens with forms, tables and `v-for` / `v-if` / `v-model`
- load a page's data in `mounted()` and keep it in `data()`
- use `computed` to filter a list
- use route params (`this.$route.params.id`), query params (`this.$route.query.q`) and watchers
- build a countdown timer with `setInterval` and clean it up

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap: store, router, api.js |
| 0:10 – 0:25 | The page pattern: `data()` → `mounted()` → `api.get` → table; why lists stay out of the store |
| 0:25 – 0:55 | Admin: `AdminDashboard` (subjects + chapters), `ChapterQuizzes`, `QuizQuestions` |
| 0:55 – 1:10 | Admin: `UsersView` (block/unblock), navbar search + `SearchView` |
| 1:10 – 1:45 | User: `UserDashboard` (filter by subject), `QuizAttempt` (timer, auto-submit), `ScoresView` |
| 1:45 – 2:00 | Full demo: create a quiz as admin → attempt as user → see score |

---

## Screens

| URL | Role | Page | What it shows |
|---|---|---|---|
| `/admin` | admin | AdminDashboard | Subject cards, each with a chapter table; one small form for add/edit |
| `/admin/chapters/:id` | admin | ChapterQuizzes | Quizzes of a chapter: title, date, duration (min), remarks |
| `/admin/quizzes/:id` | admin | QuizQuestions | Questions with 4 options, radio button marks the correct one |
| `/admin/users` | admin | UsersView | Users table, Block / Unblock |
| `/admin/search?q=` | admin | SearchView | Users, subjects, quizzes matching the text |
| `/dashboard` | user | UserDashboard | All quizzes, subject filter, Start button |
| `/quiz/:id` | user | QuizAttempt | All questions on one page, countdown, Submit, result card |
| `/scores` | user | ScoresView | Past attempts with % badge |

Styling is **Bootstrap classes only**: `card border-0 shadow-sm`, `table`, `badge`, `btn`, `form-control`, `breadcrumb`, `row/col` grid, `table-responsive`, a collapsible `navbar` for mobile.

---

## Concepts in plain words

- **Every page follows the same pattern** – no new store code today:

  ```js
  data()    { return { quizzes: [], form: null } },        // 1. empty values
  mounted() { this.loadQuizzes() },                         // 2. load when the page opens
  methods: {
    async loadQuizzes() {
      const response = await api.get('/chapters/' + this.chapterId + '/quizzes')
      this.quizzes = response.data.quizzes                  // 3. the table updates by itself
    },
    async save() { /* api.post or api.put, then */ this.loadQuizzes() },   // 4. reload after a change
  }
  ```
- **Why not put subjects and quizzes in Vuex?** Each list is shown on one page, so the page keeps it. The store stays small: only who is logged in and the message. (Rule: put something in the store only when several pages need the *same* value at the same time.)
- **Messages** – after saving: `this.$store.dispatch('showMessage', { type: 'success', text: 'Saved' })`; on an error: `{ type: 'danger', text: errorText(error) }`.
- **One form for add & edit** – `form = null` hides the form. "New" fills it with empty values; "Edit" fills it with a copy of the row. On save: if `form.id` exists → `PUT`, otherwise → `POST`.
- **URL params** – `/admin/chapters/:id` → `this.$route.params.id`. We copy it into `data()` as `chapterId`.
- **computed for filtering** – the user dashboard loads all quizzes once. `shownQuizzes()` returns only the selected subject's quizzes and is worked out again whenever the dropdown changes.
- **Timer** – `setInterval` every second decreases `secondsLeft`; at 0 we call `submit()` automatically. The `unmounted()` hook clears the interval (otherwise it keeps running after leaving the page).
- **Watcher** – on the search page, searching again from the navbar only changes `?q=` in the URL, so `watch: { '$route.query.q'() { this.search() } }` runs the search again.

---

## Build steps

| # | File | What & why |
|---|---|---|
| 1 | `views/admin/AdminDashboard.vue` | subjects with their chapters; one form for subject / chapter (replaces the Day 4 placeholder) |
| 2 | `views/admin/ChapterQuizzes.vue`, `QuizQuestions.vue` | same pattern + breadcrumbs |
| 3 | `views/admin/UsersView.vue`, `SearchView.vue` | block / unblock; search results |
| 4 | `views/user/UserDashboard.vue`, `QuizAttempt.vue`, `ScoresView.vue` | quiz list + filter, timer, scores |
| 5 | `router/index.js` | import the new pages, 6 new routes with `meta.role` |
| 6 | `components/NavBar.vue` | role-based links, admin search box, mobile hamburger (`navbar-expand-md` + `show` class toggled by Vue) |

No backend changes and no store changes today – the APIs from Day 3 are enough.

---

## Run & check

1. `python seed_demo.py` (if not done), `python app.py`, `npm run dev`
2. Admin: add subject → chapter → quiz → 2 questions; edit one; delete one
3. Search "python" from the navbar
4. Block the demo user → try to log in as that user → "Your account is blocked"
5. Unblock, log in as user, filter by subject, start a quiz, watch the timer, submit
6. Set a quiz duration of 1 minute and let it auto-submit
7. Resize the browser to phone width – navbar collapses, tables scroll sideways

## Common errors

| Error | Fix |
|---|---|
| Page shows old data after save | call the page's `load…()` method again after the API call |
| Timer keeps running on another page | clear it in the `unmounted()` hook |
| Radio buttons all select together | each question needs its own `v-model="answers[q.id]"` |
| Same page, new `:id`, no reload | Vue reuses the component – watch `'$route.params.id'` if you link between items of the same page |

## Homework

1. Show "Upcoming" vs "Past" quizzes on the user dashboard using `date_of_quiz`.
2. Add a confirmation step before submitting if some questions are unanswered.
