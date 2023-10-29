import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import AudioTranscription from '@/components/AudioTranscription.vue'
import VoiceOutput from '@/components/VoiceOutput.vue';
import ChatInput from '@/components/ChatInput.vue'; 
import Orchestration from '@/components/Orchestration.vue'; 
import VoiceTranscription from '@/components/VoiceTranscription.vue'; 
import AITalk from '@/components/AITalk.vue'; 

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home 
  },
  {
    path: '/transcribe',
    name: 'AudioTranscription',
    component: AudioTranscription
  },
  {
    path: '/voiceoutput',
    name: 'VoiceOutput',
    component: VoiceOutput
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatInput  
  },
  {
    path: '/orchestrate',
    name: 'Orchestration',
    component: Orchestration  
  },
  {
    path: '/ai-talk',
    name: 'AITalk',
    component: AITalk  
  },
  {
    path: '/voice-transcription',
    name: 'VoiceTranscription',
    component: VoiceTranscription  
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
