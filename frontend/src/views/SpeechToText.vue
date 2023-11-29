<template>
    <div class="voice-chat-area">
        オーディオファイルを選択する
        <!-- <AudioUploadArea @audio-data-uploaded="setUploadedAudioData($event)" :audio-data-list="audioDataList"/>
        オーディオ ファイル -->
        <!-- <AudioFileList :audio-data="uploadedAudioData" 
        @audio-data-selected="setSelectedAudioData($event)"
        @changed-audio-data="setAudioDataList($event)"
        /> -->
        <!-- 選択されたオーディオ ファイル
        <AudioFileDetail :audio-data="selectedAudioData"/> -->
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import AudioUploadArea from "@/components/SpeechToText/AudioUploadArea.vue";
import AudioFileList from "@/components/SpeechToText/AudioFileList.vue";
import AudioFileDetail from "@/components/SpeechToText/AudioFileDetail.vue";
import { AudioData } from "@/models/SpeechToText"

onMounted(()=>{
    
})

const uploadedAudioData = ref<AudioData | null>(null);
const selectedAudioData = ref<AudioData | null>(null);
const audioDataList = ref<AudioData[]>([]);

// function setUploadedAudioData(audioData:AudioData){
//     uploadedAudioData.value=audioData;
// }

// function setSelectedAudioData(audioData:AudioData){
//     selectedAudioData.value=audioData;
// }

// function setAudioDataList(audioDataListParam:AudioData[]){
//     audioDataList.value=audioDataListParam;
// }


</script>

<style scoped>
.voice-chat-area{
    display: flex;
    flex-direction: column;
}
</style>