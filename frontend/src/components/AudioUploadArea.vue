<template>
  <div class="voice-component">
    <label class="root-247" style="font-weight: 600"
      >オーディオファイルを選択する</label
    >
    <div class="voice-body">
      <div class="icon-wrapper">
        <img :src="cloudupload" alt="cloudupload" class="icon" />
      </div>
      <p>オーディオ ファイルをここにドラッグ アンド ドロップするか、</p>
      <button
        @click="openFileDialog"
        type="button"
        aria-label="ファイルの参照...: audio files"
        aria-disabled="false"
        class="root-404"
      >
        ファイルの参照...
      </button>
      <p />
      <div v-if="!isRecording">
        <button @click="startRecording" class="recording-button" type="button">
          <img :src="MicIcon" alt="マイクアイコン" class="icon" />
        </button>
        <p />
        <span class="css-201" style="color: inherit"
          >または
          <button
            aria-disabled="false"
            class="ms-Link root-404"
            @click="startRecording"
          >
            マイクで音声を録音する
          </button></span
        >
        <div>
          <audio v-if="audioSrc" controls :src="audioSrc"></audio>
        </div>
      </div>
      <div v-else>
        <button @click="stopRecordingAndSend" class="recording-button">
          <img :src="StopIcon" alt="StopIcon" class="icon" />
        </button>
        <p />
        <div class="ms-Stack css-411" style="align-items: center">
          <img :src="listening" alt="listening" class="icon" />
          <span class="css-201">リスニング...</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import cloudupload from "@/assets/cloudupload.svg";
import MicIcon from "@/assets/MicIcon.svg";
import StopIcon from "@/assets/StopIcon.svg";
import listening from "@/assets/listening.svg";

export default {
  data() {
    return {
      cloudupload,
      MicIcon,
      StopIcon,
      listening,
      isRecording: false,
      audioSrc: null,
    };
  },
  methods: {
    openFileDialog() {
      // ファイル選択ダイアログを開くロジック
    },
    recordVoice() {
      // 音声録音のロジック
    },
    async startRecording() {
      this.isRecording = true;
      this.audioChunks = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.mediaRecorder.ondataavailable = (event) => {
        this.audioChunks.push(event.data);
      };
      this.mediaRecorder.start();
    },
    async stopRecordingAndSend() {
      return new Promise((resolve) => {
        this.isRecording = false;
        this.mediaRecorder.onstop = async () => {
          const audioBlob = new Blob(this.audioChunks, { type: "audio/webm" });
          this.audioSrc = URL.createObjectURL(audioBlob);
          await this.sendAudioToServer(audioBlob);
          resolve();
        };
        this.mediaRecorder.stop();
        this.mediaRecorder.stream.getTracks().forEach((track) => track.stop());
      });
    },
    async sendAudioToServer(audioData) {
      const formData = new FormData();
      formData.append("audio", audioData);
      try {
        const response = await fetch(
          `${process.env.VUE_APP_API_URL}/orchestrate`,
          {
            method: "POST",
            body: formData,
            credentials: "include",
          }
        );
        if (response.ok) {
          const audioBlob = await response.blob();
          console.log('URL.createObjectURL(audioBlob)'+URL.createObjectURL(audioBlob))
          this.audioSrc = URL.createObjectURL(audioBlob);
          const audio = new Audio(this.audioSrc);
          audio.play();
        } else {
          console.error("Error during the request:", response.statusText);
        }
      } catch (err) {
        console.error("Error:", err);
      }
    },

    async onFileChange(e) {
      const file = e.target.files[0];
      this.audioSrc = URL.createObjectURL(file);
      await this.sendAudioToServer(file);
    },
  },
};
</script>

<style scoped>
.voice-body {
  border: 1px solid #ccc;
  padding: 20px;
  text-align: center;
}

.icon-wrapper img {
  width: 50px;
  height: 50px;
}

.root-404 {
  font-family: "Segoe UI", "Segoe UI Web (West European)", -apple-system,
    BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  font-size: inherit;
  font-weight: inherit;
  color: rgb(16, 110, 190);
  outline: none;
  text-decoration: underline;
  background: transparent;
  border: none;
  border-bottom: 1px solid transparent;
  cursor: pointer;
  display: inline;
  margin: 0;
  overflow: inherit;
  padding: 0;
  text-align: left;
  text-overflow: inherit;
  user-select: text;
}

.recording-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}
</style>
