import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import AI_Talk from '@/views/AITalkViews.vue'; 

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home 
  },
  {
    path: '/ai-talk',
    name: 'AITalk',
    component: AI_Talk  
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
