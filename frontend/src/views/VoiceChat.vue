<template>
    <div class="voice-chat-area">
        オーディオファイルを選択する
        <AudioUploadArea @file-uploaded="setUploadedFile($event)" :audioFiles="audioFiles"/>
        オーディオ ファイル
        <AudioFileList :file="uploadedFile" 
        @file-selected="setSelectedFile($event)"
        @changed-files="setAudioFiles($event)"
        />
        選択されたオーディオ ファイル
        <AudioFileDetail :file="selectedFile"/>
    </div>
</template>

<script setup lang="ts">
import { DefineComponent, defineComponent,ref } from 'vue';
import cloudupload from "@/assets/cloudupload.svg";
import MicIcon from "@/assets/MicIcon.svg";
import StopIcon from "@/assets/StopIcon.svg";
import listening from "@/assets/listening.svg";
import AudioUploadArea from "@/components/VoiceChat/AudioUploadArea.vue";
import AudioFileList from "@/components/VoiceChat/AudioFileList.vue";
import AudioFileDetail from "@/components/VoiceChat/AudioFileDetail.vue";

const uploadedFile = ref<File | null>(null);
const selectedFile = ref<File | null>(null);
const audioFiles = ref<File[]>([]);

function setUploadedFile(file:File){
    uploadedFile.value=file;
    console.log(uploadedFile.value.name)
}

function setSelectedFile(file:File){
    selectedFile.value=file;
}

function setAudioFiles(files:File[]){
    audioFiles.value=files;
}


</script>

<style scoped>
.voice-chat-area{
    display: flex;
    flex-direction: column;
}
</style>