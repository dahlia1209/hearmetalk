<template>
  <header>
    <nav>
      <router-link v-for="route in routes" :key="route.path" :to="route.path">
        {{ route.name }}
      </router-link>
    </nav>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent( {
  name: 'Header',
  computed: {
    routes() {
      const router = useRouter();
      // メタタグなどで表示を制御したい場合、この部分を修正します
      return router.options.routes.filter(route => !route.meta || !route.meta.hidden);
    }
  }
})
</script>

<style scoped>
/* ここにヘッダーのスタイルを追加します */
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
