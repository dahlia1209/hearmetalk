<!-- src/components/VoiceOutput.vue -->
<template>
  <div>
    <input v-model="text" placeholder="テキストを入力してください">
    <button @click="convertTextToVoice">送信</button>
    <audio v-if="audioBlob" controls :src="audioSrc"></audio>
  </div>
</template>

<script>
export default {
  data() {
    return {
      text: '',
      audioBlob: null
    };
  },
  computed: {
    audioSrc() {
      return URL.createObjectURL(this.audioBlob);
    }
  },
  methods: {
    async convertTextToVoice() {
      if (!this.text) return;
      
      const response = await fetch("http://localhost:5000/synthesize", {
        method: 'POST',
        body: JSON.stringify({ text: this.text }),
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        this.audioBlob = await response.blob();
      }
    }
  }
};
</script>
