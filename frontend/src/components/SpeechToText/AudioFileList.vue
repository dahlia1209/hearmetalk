<template>
    <div class="audio-file-list">
        <div class="div-2" v-if="audioDataList.length === 0">オーディオ ファイルがここに表示されます</div>
        <div tabindex="0" class="div-1" v-for="(audioData, index) in audioDataList" :key="audioData.audioDataId"
            :class="{ 'selected': selectedAudioDataIndex === index }" @click="audioDataSelected(audioData, index)">
            <img :src="GreenCheck" alt="GreenCheck">
            <button type="button" class="button-1" ref="filesRefs">{{
                audioData.audioFile.name
            }}</button>
            <div>
                <img :src="rotate" alt="rotate" class="svg-1" @click.stop="handleSubmitAudio(audioData, index)" v-if="recordingState==='stop'">
                <img :src="spinner" alt="spinner" class="svg-1"  v-else-if="recordingState==='pending'">
            </div>
            <img :src="TrashBin" alt="TrashBin" class="svg-1" @click.stop="removeAudioData(index)">
        </div>
    </div>
</template>

<script setup lang="ts">
import {  ref, watch } from 'vue';
import GreenCheck from "@/assets/GreenCheck.svg";
import TrashBin from "@/assets/TrashBin.svg";
import rotate from "@/assets/rotate.svg";
import spinner from "@/assets/spinner.svg";
import { submitAudio } from "@/services/speechToTextServices"
import { AudioData } from "@/models/SpeechToText"

const props = defineProps<{ audioData: AudioData | null }>()
const audioDataList = ref<AudioData[]>([]);
const filesRefs = ref<HTMLElement[]>([]);
const emit = defineEmits(['changedAudioDataList', 'audioDataSelected'])
const selectedAudioDataIndex = ref<number | null>(null)
const recordingState = ref<"recording" | "stop" | "pending">("stop");

watch(props, () => {
    if (props.audioData) {
        console.log("AudioFileList:audioData を受け取りました")
        audioDataList.value.push(props.audioData)
    }
    emit('changedAudioDataList', audioDataList.value)
})

watch(filesRefs.value, () => {
    if (filesRefs.value.length > 0) {
        filesRefs.value[filesRefs.value.length - 1].click()
    }
})

function audioDataSelected(audioData: AudioData, index: number) {
    console.log("audioDataSelected")
    console.log(audioData.text)
    selectedAudioDataIndex.value = index;
    emit('audioDataSelected', audioData)
}

function removeAudioData(index: number) {
    audioDataList.value.splice(index, 1)
    emit('changedAudioDataList', audioDataList.value)
}

async function handleSubmitAudio(audioData: AudioData, index: number) {
    try {
        recordingState.value='pending'
        const response = await submitAudio(audioData);
        console.log(response.filename)
        console.log(index)
        audioDataList.value[index] = new AudioData(audioDataList.value[index].audioDataId, response.toFile(), response.durationMs, response.filename, response.mimeType, response.fileExtension, response.text)
        emit('audioDataSelected', audioDataList.value[index])
        recordingState.value='stop'
    } catch (error) {
        console.error('Submit Error:', error);
    }
}

</script>

<style scoped>
.audio-file-list {
    display: flex;
    flex-direction: column;
    border: 1px;
    border-color: grey;
    border-style: solid;
    max-height: 100px;
    height: 100px;
    overflow: auto;
}



.button-1 {
    background-color: transparent;
    border: none;
    cursor: pointer;
    text-decoration: underline;
    color: blue;
    border-bottom: #EDEBE9;
    border-bottom: 2px solid #F3F2F1;
    font-size: 16px;
}

.div-1 {
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.div-1:hover {
    background-color: #F3F2F1;
}

.svg-1 {
    width: 16px;
    height: 16px;
}

.div-2 {
    color: #605E5C;
    margin: auto;
}

.selected {
    background-color: #F3F2F1;
}
</style>