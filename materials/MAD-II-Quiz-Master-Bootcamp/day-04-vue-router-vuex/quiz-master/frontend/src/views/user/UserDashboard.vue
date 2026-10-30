<template>
  <!-- v-if: after logout, user becomes null for a moment before we leave this page -->
  <div v-if="user">
    <h3 class="fw-semibold mb-3">Hi, {{ user.full_name }}</h3>
    <div class="card border-0 shadow-sm">
      <div class="card-body">
        <p class="mb-2">Your profile from <code>GET /api/me</code>:</p>
        <pre class="bg-light p-3 rounded small mb-0">{{ profile }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
// Day 4 placeholder: replaced by the quiz list on Day 5.
import api from '../../api'

export default {
  name: 'UserDashboard',
  data() {
    return { profile: null }
  },
  computed: {
    user() {
      return this.$store.state.user
    },
  },
  async mounted() {
    const response = await api.get('/me')
    this.profile = response.data.user
  },
}
</script>
