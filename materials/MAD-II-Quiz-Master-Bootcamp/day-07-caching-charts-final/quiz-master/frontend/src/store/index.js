// The Vuex store keeps only what MANY pages need:
//   1. who is logged in (token + user)
//   2. the message shown at the top right ("Saved", "Wrong password", …)
// Everything else (subjects, quizzes, scores…) is loaded by the page that shows it.
import { createStore } from 'vuex'
import api from '../api'

export default createStore({
  // 1. STATE – the data. Read back from localStorage so a page refresh keeps you logged in.
  state: {
    token: localStorage.getItem('token'),
    user: JSON.parse(localStorage.getItem('user')),
    message: null, // { type: 'success' | 'danger' | 'warning', text: '...' }
  },

  // 2. GETTERS – values worked out from the state
  getters: {
    isLoggedIn(state) {
      return state.token !== null
    },
    isAdmin(state) {
      return state.user !== null && state.user.roles.includes('admin')
    },
  },

  // 3. MUTATIONS – the ONLY place where state is changed (no API calls here)
  mutations: {
    setLogin(state, data) {
      state.token = data.token
      state.user = data.user
    },
    clearLogin(state) {
      state.token = null
      state.user = null
    },
    setMessage(state, message) {
      state.message = message
    },
  },

  // 4. ACTIONS – call the API (or wait), then commit a mutation
  actions: {
    async login(context, form) {
      const response = await api.post('/login', form)
      const data = response.data // { token: '...', user: {...} }
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      context.commit('setLogin', data)
    },

    async logout(context) {
      try {
        await api.post('/logout')
      } finally {
        localStorage.clear()
        context.commit('clearLogin')
      }
    },

    showMessage(context, message) {
      context.commit('setMessage', message)
      setTimeout(() => context.commit('setMessage', null), 3000) // hide after 3 seconds
    },
  },
})
