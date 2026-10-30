<script setup>
  import NavBar from './components/NavBar.vue'
  import FlashMessage from './components/FlashMessage.vue'
</script>
<template>
  <NavBar />
  <FlashMessage />
  <main class="container py-4">
    <router-view />
  </main>
</template>

<script>
export default {
  name: 'App',
}
</script>
