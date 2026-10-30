<template>
  <NavBar />
  <FlashMessage />
  <main class="container py-4">
    <router-view />
  </main>
</template>

<script>
import NavBar from './components/NavBar.vue'
import FlashMessage from './components/FlashMessage.vue'

export default {
  name: 'App',
  components: { NavBar, FlashMessage },
}
</script>
