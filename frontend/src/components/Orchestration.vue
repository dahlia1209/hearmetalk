<template>
  <div class="container">
    <div class="audio-section">
      <AudioUploadArea />
    </div>
  </div>
</template>

<script>
import MicIcon from "@/assets/MicIcon.svg";
import StopIcon from "@/assets/StopIcon.svg";
import AudioUploadArea from "./AudioUploadArea.vue";

export default {
  data() {
    return {
      MicIcon,
      StopIcon,
      mediaRecorder: null,
      audioChunks: [],
      audioSrc: "",
      transcription: "",
    };
  },
  components: {
    AudioUploadArea,

  },
  methods: {
    showInfo(file) {
      // ここにファイルの詳細情報を表示するロジックを書く
      alert(`Info for ${file.name}`);
    },
    deleteFile(file) {
      // ここにファイルの削除ロジックを書く
      const index = this.files.indexOf(file);
      if (index !== -1) {
        this.files.splice(index, 1);
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
}

.container > div:first-child {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.recording-controls {
  display: flex;
  gap: 10px;
}

.icon {
  width: 50px;
  height: 50px;
}

.audio-file {
  margin-bottom: 15px;
}

.audio-select-field {
  float: left;
  /* 他の必要なスタイルを追加 */
}

.file-list-field {
  float: left;
  margin-top: 20px; /* 必要に応じて調整 */
  /* 他の必要なスタイルを追加 */
}

.playlist-and-json-field {
  float: right;
  /* 他の必要なスタイルを追加 */
}

.audio-section {
  width: 80%;
}

.detail-section {
  width: 60%;
}
</style>
