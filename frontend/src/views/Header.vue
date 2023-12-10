<template>
  <header>
      <router-link class="router-link-1" v-for="route in routes" :key="route.path" :to="route.path">
        {{ route.name }}
      </router-link>

  </header>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useRouter, type RouteRecordRaw } from 'vue-router';

const routes = ref<RouteRecordRaw[] | null>(null)
onMounted(() => {
  const router = useRouter();
  routes.value = router.options.routes.filter(route => !route.meta || !route.meta.hidden)
})

</script>

<style scoped>
header {
  background-color: #333;
  padding: 8px 2rem;
  display: flex;
  align-items: center;
  justify-content: top;
  flex-direction: column;
}

nav a {
  margin-right: 1rem;
  color: white;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

.button-1 {
  background-color: transparent;
  color: white;
  cursor: pointer;
  outline: none;
  font-size: 24px;
  border: none;
}

.router-link-1 {
  color: white;
  font-size: 18px;
  padding: 4px;
  text-decoration: none;
}

.router-link-1:hover {
  text-decoration: underline;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
