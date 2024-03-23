<template>
  <div :class="{'div-1':responsiveType==='desktop','div-2':responsiveType==='mobile'}">
    <Header v-if="responsiveType==='desktop'" />
    <HeaderSp v-else-if="responsiveType==='mobile'" />
    <router-view />
  </div>
</template>

<script lang="ts" setup>
import Header from './views/Header.vue'
import HeaderSp from './views/HeaderSp.vue'
import { onBeforeMount, onMounted, onUnmounted, ref, watch } from 'vue';
const windowsWidth=ref(0)
const responsiveType=ref<'desktop'|'mobile'>('desktop')

onMounted(()=>{
  windowsWidth.value=window.innerWidth
  window.addEventListener('resize', ()=>windowsWidth.value=window.innerWidth);
})

onUnmounted(()=>{
  window.removeEventListener('resize', ()=>windowsWidth.value=window.innerWidth);
})

watch(windowsWidth,()=>{
  if(windowsWidth.value>=768){
    responsiveType.value='desktop'
  }else{
    responsiveType.value='mobile'
  }
})


</script>

<style scoped>
.div-1{
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
  flex-grow: 1;
}

.div-2{
  display: flex;
  flex-direction: column;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
