<script setup>
    import { RouterLink } from "vue-router";
    import store from "@/store"
</script>
<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="/" style="padding-left: 10px;">
            Flask and Vue Bootcamp
        </a>
         <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav" v-bind:style="navStyle">
            <ul class="navbar-nav" v-bind:style="navStyle">
                <li class="nav-item" v-for="course in store.getters.getCourses">
                    <RouterLink class="nav-link active" aria-current="page" :to="{name: 'course' , params: {name: course['name']}}">
                        {{ course["name"] }}
                    </RouterLink>
                </li>
            </ul>
        </div>
    </nav>
</template>
<script>
    export default {
        data(){
            return {
                navStyle: {
                    backgroundColor: "rgb(33,37,41)",
                    color: "white"
                },
                weeks: [1, 2]
            }
        }
    }
</script>