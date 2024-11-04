<script setup>
    import { RouterLink } from "vue-router";
    import store from "@/store"
</script>
<template>
    <main>
        <div style="width: 80%;">
            <div class="accordion" id="accordionCourse">
                <div class="accordion-item" v-for="each, index in courses['sessions']">
                    <h2 class="accordion-header">
                        <button :class="['accordion-button', (index) ? 'collapsed' : '']" type="button" data-bs-toggle="collapse" 
                            :data-bs-target="'#collapse'+index" aria-expanded="false" :aria-controls="'collapseOne'+index">
                            {{ each["name"] }}
                        </button>
                    </h2>
                    <div :id="'collapse'+index" :class="['accordion-collapse', 'collapse', (!index) ? 'show' : '']" 
                        data-bs-parent="#accordionExample">
                        <div class="accordion-body">
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">
                                    <RouterLink :to="{name: 'course-video', params:{video: each['youtube-video-id']}}">
                                        Video
                                    </RouterLink>
                                </li>
                                <li class="list-group-item">
                                    <RouterLink to="">Slides</RouterLink>
                                </li>
                                <li class="list-group-item">
                                    <RouterLink to="">Notes</RouterLink>
                                </li>
                                <li class="list-group-item">
                                    <a :href="courses['base-url']+each['source-code']">Source codes</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {{store.state.check}}
    </main>
</template>
<script>
    export default{
        props: ["year", "term", "name"],
        data()
        {
            return {

            };
        },
        computed:{
            courses(){
                var items = store.getters.filterCourses(this.year, this.term);
                
                items = items.filter(each => each["name"] == this.name);
                return items[0];
            }
        }
    }
</script>
<style>
    #accordionCourse{
        margin-top: 20px;
        width: 100%;
    }
    main{
        display: flex;
        justify-content: center;
    }
</style>