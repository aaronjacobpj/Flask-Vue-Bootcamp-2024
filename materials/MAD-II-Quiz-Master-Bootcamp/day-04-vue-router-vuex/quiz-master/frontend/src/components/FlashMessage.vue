<template>
  <div v-if="message" class="alert shadow-sm position-fixed top-0 end-0 mt-5 me-3 z-3" :class="'alert-' + message.type">
    {{ message.text }}
  </div>
</template>

<script>
// Shows store.state.message. Any page can set it with:
//   this.$store.dispatch('showMessage', { type: 'success', text: 'Saved' })
export default {
  name: 'FlashMessage',
  data() {
    return {
    }
  },
  computed: {
    message() {
      return this.$store.state.message
    },
  },
}
</script>

