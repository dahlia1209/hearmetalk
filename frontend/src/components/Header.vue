<template>
  <header>
    <nav>
      <router-link v-for="route in routes" :key="route.path" :to="route.path">
        {{ route.name }}
      </router-link>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'Header',
  computed: {
    routes() {
      // メタタグなどで表示を制御したい場合、この部分を修正します
      return this.$router.options.routes.filter(route => !route.meta || !route.meta.hidden);
    }
  }
}
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
