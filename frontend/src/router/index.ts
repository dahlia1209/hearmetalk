import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import AI_Talk from '@/views/AITalkViews.vue'; 
import Live from '@/views/LiveViews.vue'; 
import OAuth2 from '@/views/OAuth2.vue'; 

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
  {
    path: '/live',
    name: 'Live',
    component: Live  
  },
  {
    path: '/oauth2callback',
    name: 'OAuth2',
    component: OAuth2  
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
