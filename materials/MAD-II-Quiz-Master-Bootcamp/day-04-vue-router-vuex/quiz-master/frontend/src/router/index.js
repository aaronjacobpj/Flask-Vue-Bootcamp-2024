import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import NotFound from '../views/NotFound.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import UserDashboard from '../views/user/UserDashboard.vue'

// meta.role says who may open the page
const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/admin', component: AdminDashboard, meta: { role: 'admin' } },
  { path: '/dashboard', component: UserDashboard, meta: { role: 'user' } },
  { path: '/:pathMatch(.*)*', component: NotFound }, // any other URL
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
