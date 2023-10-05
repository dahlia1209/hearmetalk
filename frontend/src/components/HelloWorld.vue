<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: 'Loading...'
    };
  },
  created() {
    axios.get('http://localhost:5000/api/message')
      .then(response => {
        this.message = response.data.message;
      })
      .catch(error => {
        console.error('An error occurred:', error);
        this.message = 'An error occurred';
      });
  }
};
</script>
