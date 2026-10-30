// One axios object for the whole app. Every page does:  import api from '../api'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
})

// Before every request: add the login token (saved in localStorage by the store)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers['Authentication-Token'] = token
  return config
})

// After every response: if the token is no longer valid (401), log out and go to the login page
api.interceptors.response.use(
  (response) => response, // success: nothing to do
  (error) => {
    const status = error.response && error.response.status
    if (status === 401 && localStorage.getItem('token')) {
      localStorage.clear()
      window.location.href = '/login' // full reload -> the store starts empty
    }
    return Promise.reject(error)
  },
)

// Get a readable message out of an error, e.g. "Invalid email or password"
export function errorText(error) {
  if (error.response && error.response.data && error.response.data.message) {
    return error.response.data.message
  }
  return error.message
}

export default api
