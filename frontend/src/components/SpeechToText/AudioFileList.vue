<template>
    <div class="audio-file-list">
        <div class="div-2" v-if="audioDataList.length === 0">オーディオ ファイルがここに表示されます</div>
        <div tabindex="0" class="div-1" v-for="(audioData, index) in audioDataList" :key="audioData.audioDataId"
            :class="{ 'selected': selectedAudioDataIndex === index }" @click="audioDataSelected(audioData, index)">
            <img src="@/assets/GreenCheck.svg" alt="GreenCheck">
            <button type="button" class="button-1" ref="filesRefs">{{
                audioData.audioFile.name
            }}</button>
            <div>
                <img src="@/assets/rotate.svg" alt="rotate" class="svg-1" @click.stop="handleSubmitAudio(audioData, index)" v-if="isWaitingRefs[index]" ref="isWaitingRefs">
                <img src="@/assets/spinner.svg" alt="spinner" class="svg-1"  v-else>
            </div>
            <img src="@/assets/TrashBin.svg" alt="TrashBin" class="svg-1" @click.stop="removeAudioData(index)">
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { submitAudio } from "@/services/speechToTextServices"
import { AudioData } from "@/models/SpeechToText"

const props = defineProps<{ audioData: AudioData | null }>()
const audioDataList = ref<AudioData[]>([]);
const filesRefs = ref<HTMLElement[]>([]);
const isWaitingRefs = ref<boolean[]>([]);
const emit = defineEmits(['changedAudioDataList', 'audioDataSelected'])
const selectedAudioDataIndex = ref<number | null>(null)
// const recordingState = ref<"recording" | "stop" | "pending">("stop");

watch(props, () => {
    if (props.audioData) {
        audioDataList.value.push(props.audioData)
        isWaitingRefs.value.push(true)
    }
    emit('changedAudioDataList', audioDataList.value)
})

watch(filesRefs.value, () => {
    if (filesRefs.value.length > 0) {
        filesRefs.value[filesRefs.value.length - 1].click()
    }
})

function audioDataSelected(audioData: AudioData, index: number) {
    selectedAudioDataIndex.value = index;
    emit('audioDataSelected', audioData)
}

function removeAudioData(index: number) {
    audioDataList.value.splice(index, 1)
    emit('changedAudioDataList', audioDataList.value)
}

async function handleSubmitAudio(audioData: AudioData, index: number) {
    try {
        isWaitingRefs.value[index]=false
        const response = await submitAudio(audioData);
        audioData.text=response.text;
        emit('audioDataSelected', audioDataList.value[index])
        isWaitingRefs.value[index]=true
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