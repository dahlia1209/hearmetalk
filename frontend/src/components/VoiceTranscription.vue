<template>
  <div>
    <!-- 音声の録音を開始するボタン -->
    <button @click="startRecording">Start Recording</button>
    <!-- 音声の録音を終了して音声をサーバに送信するボタン -->
    <button @click="stopRecordingAndSend">Stop Recording</button>

    <!-- 音声のテキスト変換結果を表示する部分 -->
    <div v-if="transcription">{{ transcription }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mediaRecorder: null,
      audioChunks: [],
      transcription: "",
    };
  },
  methods: {
    async startRecording() {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.mediaRecorder.ondataavailable = (event) => {
        this.audioChunks.push(event.data);
      };
      this.mediaRecorder.start();
    },
    async stopRecordingAndSend() {
      return new Promise((resolve) => {
        this.mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(this.audioChunks, { type: "audio/webm" });
          const formData = new FormData();
          formData.append("audio", audioBlob);
          try {
            const response = await fetch("http://localhost:5000/recognize", {
              method: "POST",
              body: formData,
            });
            const data = await response.json();
            if (data.text) {
              this.transcription = data.text;
            }
            resolve();
          } catch (err) {
            console.error("Error:", err);
          }
        };
        this.mediaRecorder.stop();
        this.mediaRecorder.stream.getTracks().forEach((track) => track.stop());
      });
    },
  },
};
</script>
