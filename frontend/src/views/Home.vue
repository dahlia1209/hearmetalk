<template>
  <div class="home-view">
    <Profile v-if="homeState.currentView==='profile'"  />
    <Talking v-else-if="homeState.currentView==='talking'"/>
  </div>
</template>

<script setup lang="ts">
import Profile from "@/components/Home/Profile.vue";
import Talking from "@/components/Home/Talking.vue";
import  { onMounted,ref } from "vue";
import { homeState } from '@/store/homeState'

// const currentView=ref<"profile" | "talking" >("profile")
onMounted(()=>{
  homeState.currentView="profile"
})
</script>
<style scoped>
.home-view{
  display: flex;
  width: 100%;
  height: 100%;
}
</style>