<template>
  <ul>
    <li v-for="(item, index) in items"> {{index}}). {{ item }} </li>
  </ul>
</template>
<script>
  export default {
    data(){
      return {
        items: ["Foo", "Bar", "Baz"]
      }
    },
    methods: {
      change(){
        this.state = false
      }
    }
  }
</script>