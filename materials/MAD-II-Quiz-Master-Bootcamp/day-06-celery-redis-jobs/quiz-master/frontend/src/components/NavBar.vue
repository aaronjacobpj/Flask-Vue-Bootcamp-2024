<template>
  <nav class="navbar navbar-expand-md navbar-dark bg-primary">
    <div class="container">
      <router-link class="navbar-brand fw-semibold" to="/">Quiz Master</router-link>

      <!-- hamburger button for small screens: just shows / hides the menu -->
      <button v-if="isLoggedIn" class="navbar-toggler" @click="menuOpen = !menuOpen">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div v-if="isLoggedIn" class="collapse navbar-collapse" :class="{ show: menuOpen }">
        <ul v-if="isAdmin" class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link" to="/admin">Subjects</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/admin/users">Users</router-link></li>
        </ul>
        <ul v-else class="navbar-nav me-auto">
          <li class="nav-item"><router-link class="nav-link" to="/dashboard">Quizzes</router-link></li>
          <li class="nav-item"><router-link class="nav-link" to="/scores">My Scores</router-link></li>
        </ul>

        <form v-if="isAdmin" class="d-flex me-md-3 my-2 my-md-0" @submit.prevent="search">
          <input v-model="searchText" class="form-control form-control-sm" placeholder="Search users, subjects, quizzes" />
        </form>

        <span class="text-white-50 small me-3">{{ user.full_name }}</span>
        <button class="btn btn-sm btn-outline-light" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      menuOpen: false,
      searchText: '',
    }
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn
    },
    isAdmin() {
      return this.$store.getters.isAdmin
    },
    user() {
      return this.$store.state.user
    },
  },
  watch: {
    // close the mobile menu after moving to another page
    $route() {
      this.menuOpen = false
    },
  },
  methods: {
    search() {
      // goes to /admin/search?q=<text>
      this.$router.push({ path: '/admin/search', query: { q: this.searchText } })
    },
    async logout() {
      await this.$store.dispatch('logout')
      this.$router.push('/login')
    },
  },
}
</script>
