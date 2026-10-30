<template>
  <div class="card border-0 shadow-sm col-12 col-md-6 col-lg-4 mx-auto mt-5">
    <div class="card-body p-4">
      <h4 class="mb-1">Create account</h4>
      <p class="text-muted small mb-4">Register as a quiz taker</p>

      <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

      <form @submit.prevent="register">
        <div class="mb-3">
          <label class="form-label">Full name</label>
          <input v-model="form.full_name" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input v-model="form.email" type="email" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password <span class="text-muted small">(min 6 chars)</span></label>
          <input v-model="form.password" type="password" minlength="6" class="form-control" required />
        </div>
        <div class="row">
          <div class="col mb-3">
            <label class="form-label">Qualification</label>
            <input v-model="form.qualification" class="form-control" />
          </div>
          <div class="col mb-3">
            <label class="form-label">Date of birth</label>
            <input v-model="form.dob" type="date" class="form-control" />
          </div>
        </div>
        <button class="btn btn-primary w-100">Register</button>
      </form>

      <p class="text-center small mt-3 mb-0">
        Already registered? <router-link to="/login">Login</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api, { errorText } from '../api'

export default {
  name: 'RegisterView',
  data() {
    return {
      form: { full_name: '', email: '', password: '', qualification: '', dob: '' },
      error: '',
    }
  },
  methods: {
    async register() {
      this.error = ''
      try {
        await api.post('/register', this.form)
        this.$store.dispatch('showMessage', { type: 'success', text: 'Registered! Please log in.' })
        this.$router.push('/login')
      } catch (error) {
        this.error = errorText(error)
      }
    },
  },
}
</script>
