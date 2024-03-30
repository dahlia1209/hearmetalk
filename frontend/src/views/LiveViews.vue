<template>
    <div class="home-view">
      <ChatList  />
    </div>
  </template>
  
  <script setup lang="ts">
  import ChatList from "@/components/Live/ChatList.vue";
  import  { onMounted,ref } from "vue";
  import { homeState } from '@/store/homeState'
  
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