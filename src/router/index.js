import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '../views/HomeView.vue';
import CourseView from "@/views/CourseView.vue";
import CourseVideoView from "@/views/CourseVideoView.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/course/:name',
      name: 'course',
      component: CourseView,
      props: true,
    },
    {
      path: '/course/:name/video/:video',
      name: 'course-video',
      component: CourseVideoView,
      props: true
    },
  ]
})

export default router
