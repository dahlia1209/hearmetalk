<template>
  <div>
    <h2>音声アップロード</h2>
    <input type="file" ref="audioInput" />
    <button @click="submitAudio">送信</button>
    <audio v-if="audioSrc" controls :src="audioSrc"></audio>
  </div>
</template>

<script>
export default {
  data() {
    return {
      audioSrc: null
    };
  },
  methods: {
    async submitAudio() {
      const audioFile = this.$refs.audioInput.files[0];
      const formData = new FormData();
      formData.append('audio', audioFile);

      try {
        const response = await fetch("http://localhost:5000/orchestrate", {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const audioBlob = await response.blob();
          this.audioSrc = URL.createObjectURL(audioBlob);
        } else {
          console.error('Error during the request:', response.statusText);
        }
      } catch (error) {
        console.error('There was an error sending the request:', error);
      }
    }
  }
};
</script>

<style scoped>
/* ここにスタイルを追加することができます */
</style>
