<template>
  <!-- v-if: after logout, user becomes null for a moment before we leave this page -->
  <div v-if="user">
    <h3 class="fw-semibold mb-3">Admin Dashboard</h3>
    <div class="card border-0 shadow-sm">
      <div class="card-body">
        <p class="mb-2">Logged in as <strong>{{ user.email }}</strong> (roles: {{ user.roles.join(', ') }})</p>
        <p class="mb-0 text-muted">Admin-only API says: <code>{{ message }}</code></p>
      </div>
    </div>
  </div>
</template>

<script>
// Day 4 placeholder: proves the token is sent and only the admin gets in.
// It is replaced by the real subjects page on Day 5.
import api, { errorText } from '../../api'

export default {
  name: 'AdminDashboard',
  data() {
    return { message: '…' }
  },
  computed: {
    user() {
      return this.$store.state.user
    },
  },
  async mounted() {
    try {
      const response = await api.get('/admin/ping')
      this.message = response.data.message
    } catch (error) {
      this.message = errorText(error)
    }
  },
}
</script>
