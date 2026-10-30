# Day 4 – Vue 3 frontend: Router, Vuex & login

**Goal:** a Vue app where users register and log in, the token is kept in a small Vuex store, and pages are protected by role.

**By the end, students can**
- create a Vue 3 project with Vite and understand its files
- use Vue Router (routes and one navigation guard)
- use Vuex (state, getters, mutations, actions) – **one store file, nothing more**
- call the API with axios and send the token automatically

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap: the API is ready; now the UI |
| 0:10 – 0:30 | Create the project, tour of `index.html`, `main.js`, `App.vue`, a `.vue` file (template / script) written with the **Options API** |
| 0:30 – 0:45 | `api.js`: one axios object + two interceptors |
| 0:45 – 1:05 | Vuex: draw the flow, write `store/index.js` |
| 1:05 – 1:30 | Router + guard, Login and Register pages, NavBar, FlashMessage |
| 1:30 – 1:50 | Placeholder dashboards that call `/api/me` and `/api/admin/ping` |
| 1:50 – 2:00 | Demo: login as user & admin, try to open `/admin` as user |

---

## Create the project

```bash
cd quiz-master
npm create vite@latest frontend -- --template vue
cd frontend
npm install
npm install vue-router@4 vuex@4 axios bootstrap
npm run dev           # http://localhost:5173
```

Delete the template's demo files (`src/components/HelloWorld.vue`, `src/style.css`, `src/assets/`) – we write our own.

Bootstrap is installed with **npm** and imported once in `main.js` – no CDN links, no custom CSS file:

```js
import 'bootstrap/dist/css/bootstrap.min.css'
```

(Start Flask in another terminal: `python app.py`.)

---

## The frontend in one picture

```
main.js ──► App.vue = <NavBar/> + <FlashMessage/> + <router-view/>
                                                      │
router/index.js  decides WHICH page goes into <router-view/>
store/index.js   remembers WHO is logged in (+ the message on screen)
api.js           talks to Flask (adds the token to every request)
views/*.vue      the pages – each page loads its own data with api.get(...)
```

Rule we follow all week: **the store only keeps what many pages need** (the logged-in user and the message). Subjects, quizzes, scores … are loaded by the page that shows them and kept in that page's `data()`.

---

## Concepts in plain words

- **SPA** – the browser loads one page; Vue swaps components when the URL changes. No full page reloads.
- **Options API** – every component is one object, with each kind of code in its own named section:

  ```js
  export default {
    name: 'LoginView',
    data() { return { form: { email: '', password: '' }, error: '' } },  // the page's own values
    computed: { },              // values worked out from other values
    mounted() { },              // runs once the page is on screen (load data here)
    methods: { async login() { /* this.form, this.error … */ } },
  }
  ```
  Inside the object everything is reached through `this`: `this.form`, `this.$store`, `this.$router` (to change page), `this.$route` (current URL). In the template you leave out `this`. Write methods as normal functions (`login() {}`), not arrow functions, so `this` is the component.

- **api.js** – one axios object with `baseURL = http://localhost:5000/api`, so pages write `api.get('/me')`.
  - *Request interceptor* – runs before every request: reads the token from `localStorage` and adds the `Authentication-Token` header.
  - *Response interceptor* – runs after every response: on **401** (token no longer valid) it clears `localStorage` and goes to `/login`.
  - `errorText(error)` – gets the server's message ("Invalid email or password") out of an axios error.

- **Vuex** – one shared object for data many components need. Four parts, always in this order:

  | Part | What it is | Our store |
  |---|---|---|
  | `state` | the data | `token`, `user`, `message` |
  | `getters` | values worked out from state | `isLoggedIn`, `isAdmin` |
  | `mutations` | the **only** functions that change state – no API calls | `setLogin`, `clearLogin`, `setMessage` |
  | `actions` | call the API (or wait), then **commit** a mutation | `login`, `logout`, `showMessage` |

  ```
  page ──dispatch('login', form)──► action ──api.post('/login')──► Flask
                                       └──commit('setLogin', data)──► mutation ──► state ──► every page updates
  ```

  Using the store from a page:

  | Want to… | Write |
  |---|---|
  | read state | `this.$store.state.user` |
  | read a getter | `this.$store.getters.isAdmin` |
  | run an action | `this.$store.dispatch('login', this.form)` |
  | show a message | `this.$store.dispatch('showMessage', { type: 'success', text: 'Saved' })` |

  To use a store value in the template, wrap it in a `computed`:
  ```js
  computed: {
    user() { return this.$store.state.user },
  }
  ```

- **Why also localStorage?** The store is emptied when the page is refreshed. The `login` action also saves `token` and `user` in `localStorage`, and the store's `state` reads them back when the app starts. `logout` removes them.

- **Vue Router** – a list of `{ path, component }`. `meta: { role: 'admin' }` marks pages only the admin may open.
- **Navigation guard** – `router.beforeEach((to) => { … })` runs before every page change. Return a path to send the user somewhere else; return nothing to allow it. (This is only for user experience – the **real** security is the backend check from Day 2.)

---

## Build steps

| # | File | What & why |
|---|---|---|
| 1 | `package.json`, `vite.config.js`, `index.html` | from the Vite template (port 5173) |
| 2 | `src/main.js` | import Bootstrap CSS, `createApp(App).use(store).use(router).mount('#app')` |
| 3 | `src/api.js` | axios object, request + response interceptor, `errorText()` |
| 4 | `src/store/index.js` | state, getters, mutations, actions (whole file ≈ 60 lines) |
| 5 | `src/router/index.js` | routes + `beforeEach` guard |
| 6 | `src/App.vue` | `<NavBar/>`, `<FlashMessage/>`, `<router-view/>` |
| 7 | `src/components/NavBar.vue`, `FlashMessage.vue` | user name + logout button; message box |
| 8 | `src/views/LoginView.vue`, `RegisterView.vue` | forms with `v-model`, HTML5 validation (`required`, `type="email"`, `minlength`) and the server's error message |
| 9 | `src/views/admin/AdminDashboard.vue`, `user/UserDashboard.vue`, `NotFound.vue` | placeholders that prove the token works |

Who calls what: **Login** uses the store (`dispatch('login')`) because every page needs to know who logged in. **Register** calls `api.post('/register')` directly – nothing needs to be remembered afterwards.

---

## Run & check

1. Register a new user → message "Registered! Please log in."
2. Log in as the user → `/dashboard` shows the `/api/me` JSON
3. Type `/admin` in the address bar → sent back to `/dashboard`
4. Log out, log in as admin → `/admin` shows "Hello admin Quiz Master"
5. Refresh the page → still logged in (localStorage)
6. DevTools → Network → see the `Authentication-Token` request header
7. DevTools → Application → Local Storage → see `token` and `user`; delete them and refresh → back to login

## Common errors

| Error | Fix |
|---|---|
| CORS error in console | Flask not running, or `FRONTEND_ORIGIN` ≠ `http://localhost:5173` |
| `[vuex] unknown action type` | spelling: `dispatch('login')` must match the name under `actions` |
| `[vuex] do not mutate vuex store state outside mutation handlers` | change state only inside a mutation, using `commit` |
| Logged out after refresh | the `login` action must write `token` and `user` to localStorage |
| `Cannot read properties of null (reading 'full_name')` | `user` is `null` after logout – show it only with `v-if="user"` or `v-if="isLoggedIn"` |
| `Cannot read properties of undefined` inside a method | the method was written as an arrow function – use `login() { … }` so `this` is the component |
| Screen does not update | the value was not declared in `data()` – declare every field there first |

## Homework

1. Add a "Profile" page that shows the user's details from `this.$store.state.user` (no API call).
2. Explain to a friend in 3 lines: action vs mutation.
