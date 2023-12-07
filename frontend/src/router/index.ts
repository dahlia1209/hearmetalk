import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Chat from '@/views/Chat.vue'; 
import VoiceChat from '@/views/VoiceChatView.vue'; 
import Speech_to_Text from '@/views/SpeechToText.vue'; 
import Text_to_Speech from '@/views/TextToSpeechView.vue'; 

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home 
  },
  {
    path: '/speech-to-text',
    name: 'SpeechToText',
    component: Speech_to_Text 
  },
  {
    path: '/text-to-speech',
    name: 'TextToSpeech',
    component: Text_to_Speech 
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat  
  },
  {
    path: '/voice-chat',
    name: 'VoiceChat',
    component: VoiceChat  
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
