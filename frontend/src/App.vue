<template>
  <div>
    <Header v-if="responsiveType==='desktop'" />
    <HeaderSp v-else-if="responsiveType==='mobile'" />
    <router-view />
  </div>
</template>

<script lang="ts" setup>
import { resize } from './utils/htmlElementUtils';
import Header from './views/Header.vue'
import HeaderSp from './views/HeaderSp.vue'
import { onMounted, ref, watch } from 'vue';
const windowsWidth=ref(window.innerWidth)
const responsiveType=ref<'desktop'|'mobile'>('desktop')

onMounted(()=>{
  window.addEventListener('resize', ()=>windowsWidth.value=window.innerWidth);
})

watch(windowsWidth,()=>{
  console.log("検知しました。")
  if(windowsWidth.value>=768){
    responsiveType.value='desktop'
  }else{
    responsiveType.value='mobile'
  }
})


</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
