<template>
  <div>
    <h1>Audio Transcription</h1>
    <input type="file" @change="handleFileChange" accept="audio/*" />
    <button @click="submitAudio" :disabled="!selectedFile">Submit</button>
    <p v-if="transcription">Transcription: {{ transcription }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedFile: null,
      transcription: null,
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    submitAudio() {
      const formData = new FormData();
      formData.append("audio", this.selectedFile);

      axios
        .post("http://localhost:5000/recognize", formData, { 
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log(response.data)
          this.transcription = response.data.text;
        })
        .catch((error) => {
          console.error("An error occurred:", error);
        });
    },
  },
};
</script>
