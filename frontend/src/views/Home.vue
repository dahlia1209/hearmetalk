<template>
  <div>
    <h1>Hello world</h1>
  </div>
</template>

<script lang="ts" >
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent( {
  data() {
    return {
      message: 'Hello world...'
    };
  },
  created() {
  }
});
</script>
