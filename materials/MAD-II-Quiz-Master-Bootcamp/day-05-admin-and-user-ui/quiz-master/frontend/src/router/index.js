import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import NotFound from '../views/NotFound.vue'

import AdminDashboard from '../views/admin/AdminDashboard.vue'
import ChapterQuizzes from '../views/admin/ChapterQuizzes.vue'
import QuizQuestions from '../views/admin/QuizQuestions.vue'
import UsersView from '../views/admin/UsersView.vue'
import SearchView from '../views/admin/SearchView.vue'

import UserDashboard from '../views/user/UserDashboard.vue'
import QuizAttempt from '../views/user/QuizAttempt.vue'
import ScoresView from '../views/user/ScoresView.vue'

// meta.role says who may open the page
const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },

  // admin pages
  { path: '/admin', component: AdminDashboard, meta: { role: 'admin' } },
  { path: '/admin/chapters/:id', component: ChapterQuizzes, meta: { role: 'admin' } },
  { path: '/admin/quizzes/:id', component: QuizQuestions, meta: { role: 'admin' } },
  { path: '/admin/users', component: UsersView, meta: { role: 'admin' } },
  { path: '/admin/search', component: SearchView, meta: { role: 'admin' } },

  // user pages
  { path: '/dashboard', component: UserDashboard, meta: { role: 'user' } },
  { path: '/quiz/:id', component: QuizAttempt, meta: { role: 'user' } },
  { path: '/scores', component: ScoresView, meta: { role: 'user' } },

  // any other URL
  { path: '/:pathMatch(.*)*', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})

// Runs before every page change. Return a path to send the user somewhere else.
router.beforeEach((to) => {
  const isLoggedIn = store.getters.isLoggedIn
  const isAdmin = store.getters.isAdmin
  const home = isAdmin ? '/admin' : '/dashboard'

  if (to.path === '/login' && isLoggedIn) return home // already logged in
  if (to.meta.role && !isLoggedIn) return '/login' // must log in first
  if (to.meta.role === 'admin' && !isAdmin) return home // users can't open admin pages
  if (to.meta.role === 'user' && isAdmin) return home // the admin has his own pages
})

export default router
