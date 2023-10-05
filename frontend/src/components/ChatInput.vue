<!-- src/components/ChatInput.vue -->
<template>
  <div>
    <input v-model="userInput" placeholder="メッセージを入力してください">
    <button @click="submitText">送信</button>
    <div v-if="responseText">{{ responseText }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: '',
      responseText: ''
    };
  },
  methods: {
    async submitText() {
      const response = await fetch("http://localhost:5000/chat", {
        method: 'POST',
        body: JSON.stringify({ text: this.userInput }),
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include' 
      });

      if (response.ok) {
        const data = await response.json();
        this.responseText = data.text;  
      }
    }
  }
};
</script>
