<template>
  <nav class="navbar navbar-dark bg-primary">
    <div class="container">
      <router-link class="navbar-brand fw-semibold" to="/">Quiz Master</router-link>

      <div v-if="isLoggedIn">
        <span class="text-white-50 small me-3">{{ user.full_name }}</span>
        <button class="btn btn-sm btn-outline-light" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn
    },
    user() {
      return this.$store.state.user
    },
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logout')
      this.$router.push('/login')
    },
  },
}
</script>
