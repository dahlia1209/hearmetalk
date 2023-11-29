import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import Chat from '../views/Chat.vue'; 
import Speech_to_Text from '../views/SpeechToText.vue'; 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/speech-to-text',
      name: 'SpeechToText',
      component: Speech_to_Text
    },
  ]
})

export default router
