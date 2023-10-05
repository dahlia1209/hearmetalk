<template>
  <div>
    <!-- 音声の録音を開始するボタン -->
    <button @click="startRecording">Start Recording</button>
    <!-- 音声の録音を終了するボタン -->
    <button @click="stopRecording">Stop Recording</button>
    <!-- 音声をテキストに変換するボタン -->
    <button @click="submitAudio">Submit Audio</button>

    <!-- 音声データを再生するためのaudioタグ -->
    <audio v-if="audioURL" :src="audioURL" controls></audio>

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
      audioURL: null, // 音声データのURLを保持するためのデータ属性
    };
  },
  methods: {
    // 録音を開始
    async startRecording() {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.audioChunks = [];
      this.mediaRecorder.ondataavailable = (event) => {
        this.audioChunks.push(event.data);
      };

      // onstopイベントハンドラを追加
      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
        this.audioURL = URL.createObjectURL(audioBlob);
      };

      this.mediaRecorder.start();
    },
    // 録音を停止
    stopRecording() {
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();

        const stream = this.mediaRecorder.stream;
        const tracks = stream.getTracks();
        tracks.forEach((track) => track.stop());
      }
    },
    // サーバーに音声データを送信してテキストに変換
    async submitAudio() {
      if (this.audioChunks.length > 0) {
        const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
        const formData = new FormData();
        formData.append("audio", audioBlob);

        // ここでバックエンドAPIに音声データを送信
        const response = await fetch("http://localhost:5000/transcribe", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          this.transcription = data.transcription;
        } else {
          console.error("Failed to transcribe audio");
        }
      }
    },
  },
};
</script>
