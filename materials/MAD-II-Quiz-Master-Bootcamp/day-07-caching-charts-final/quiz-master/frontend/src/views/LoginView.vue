<template>
  <div class="card border-0 shadow-sm col-12 col-md-6 col-lg-4 mx-auto mt-5">
    <div class="card-body p-4">
      <h4 class="mb-1">Welcome back</h4>
      <p class="text-muted small mb-4">Log in to Quiz Master</p>

      <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

      <form @submit.prevent="login">
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="form.email" type="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="form.password" type="password" class="form-control" required />
        </div>
        <button class="btn btn-primary w-100">Login</button>
      </form>

      <p class="text-center small mt-3 mb-0">
        New here? <router-link to="/register">Create an account</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { errorText } from '../api'

export default {
  name: 'LoginView',
  data() {
    return {
      form: { email: '', password: '' },
      error: '',
    }
  },
  methods: {
    async login() {
      this.error = ''
      try {
        await this.$store.dispatch('login', this.form) // store action calls POST /api/login
        if (this.$store.getters.isAdmin) {
          this.$router.push('/admin')
        } else {
          this.$router.push('/dashboard')
        }
      } catch (error) {
        this.error = errorText(error)
      }
    },
  },
}
</script>
