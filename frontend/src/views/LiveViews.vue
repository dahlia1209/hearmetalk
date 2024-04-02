<template>
    <div class="home-view">
      <ChatList v-if="liveState.currentView==='chatList'" />
      <Animation v-else-if="liveState.currentView==='animation'" />
    </div>
  </template>
  
  <script setup lang="ts">
  import ChatList from "@/components/Live/ChatList.vue";
  import Animation from "@/components/Live/Animation.vue";
  import  { onMounted,ref } from "vue";
  import { liveState } from "@/store/liveState"
  
  // const currentView=ref<"profile" | "talking" >("profile")
  onMounted(()=>{

  })
  </script>
  <style scoped>
  .home-view{
    display: flex;
    width: 100%;
    height: 100%;
  }
  </style>