import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '../views/HomeView.vue';
import CourseView from "@/views/CourseView.vue";
import CourseVideoView from "@/views/CourseVideoView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main-home',
      component: HomeView,
      props: true
    },
    {
      path: '/:year/:term',
      name: 'home',
      component: HomeView,
      props: true,
    },
    {
      path: '/:year/:term/course/:name',
      name: 'course',
      component: CourseView,
      props: true,
    },
    {
      path: '/:year/:term/course/:name/video/:video',
      name: 'course-video',
      component: CourseVideoView,
      props: true
    },
  ]
})

export default router
