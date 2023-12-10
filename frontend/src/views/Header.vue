<template>
  <header>
    <nav>
      <router-link v-for="route in routes" :key="route.path" :to="route.path">
        {{ route.name }}
      </router-link>
    </nav>
  </header>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useRouter,type RouteRecordRaw } from 'vue-router';

const routes=ref<RouteRecordRaw[]|null>(null)
onMounted(()=>{
  const router=useRouter();
  routes.value=router.options.routes.filter(route => !route.meta || !route.meta.hidden)
})

</script>

<style scoped>
header {
  background-color: #333;
  color: white;
  padding: 1rem 2rem;
}

nav a {
  margin-right: 1rem;
  color: white;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}
</style>
