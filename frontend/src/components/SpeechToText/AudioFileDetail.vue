<template>
    <div class="audio-file-Detail">
        <div class="div-1">
            <div>ファイル名：{{ audioData?.audioFile.name }}</div>
            <div>言語：</div>
        </div>
        <div class="div-2">
            <div>
                <img :src="replayButton" alt="replayButton" class="svg-1" @click="playAudio()" v-if="!isPlaying">
                <img :src="stopReplay" alt="stopReplay" class="svg-1" @click="stopAudio()" v-else>
            </div>
            <audio ref="audioPlayer" @timeupdate="updateSlider" @ended="handleEnded()"></audio>

            <div>{{ formatTime(currentTime) }}</div>
            <input type="range" min="0" :max="duration" v-model="currentTime" @input="seekAudio">
            <div>{{ formatTime(duration) }}s</div>
        </div>
        <div class="div-3" v-if="audioData === null">サンプル音声をアップロードすると、ここに音声テキスト変換の結果が表示されます。</div>
        <div v-else>{{ audioData.text }}</div>
    </div>
</template>

<script setup lang="ts">
import {ref, watch,onMounted  } from 'vue';
import replayButton from "@/assets/replayButton.svg";
import stopReplay from "@/assets/stopReplay.svg";
import { AudioData } from "@/models/SpeechToText"

const props = defineProps<{ audioData: AudioData | null }>()
const audioData = ref<AudioData | null>(null);
const audioPlayer = ref<HTMLAudioElement | null>(null)
const isPlaying = ref(false)
const duration = ref(0)
const currentTime = ref(0)

watch(props, async () => {
    if (props.audioData) {
        audioData.value = props.audioData
        duration.value = audioData.value.durationMs/1000
    }
    if (audioPlayer.value && audioData.value) {
        const audioUrl = URL.createObjectURL(audioData.value.audioFile);
        audioPlayer.value.src = audioUrl;
    }
})

async function getFileDuration() {
    if (audioData.value) {
        duration.value = audioData.value.durationMs / 1000
    }
}

function playAudio() {
    if (audioData.value && audioPlayer.value) {
        isPlaying.value = true;
        audioPlayer.value.play();
    }
}

function stopAudio() {
    if (audioData.value && audioPlayer.value) {
        isPlaying.value = false;
        audioPlayer.value.pause();
    }
}

function updateSlider() {
    if (audioPlayer.value) {
        currentTime.value = audioPlayer.value.currentTime;
    }
}

function seekAudio() {
    if (audioPlayer.value) {
        audioPlayer.value.currentTime = currentTime.value;
    }
}

function formatTime(seconds: number) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);

    const hh = h < 10 ? `0${h}` : h;
    const mm = m < 10 ? `0${m}` : m;
    const ss = s < 10 ? `0${s}` : s;

    return h > 0 ? `${hh}:${mm}:${ss}` : `${mm}:${ss}`;
}

function handleEnded(){
    isPlaying.value = false
    currentTime.value=0
}

</script>

<style scoped>
.audio-file-Detail {
    border: 2px solid;
    flex-direction: column;
    border-color: #605E5C;
    padding: 12px;
    max-height: 300px;
    height: 300px;
}

.div-1 {
    display: flex;
    justify-content: space-between;
}

.div-2 {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 2px solid;
    border-color: #EDEBE9;
}

.div-3 {
    color: #605E5C;
    margin: auto;
}

.svg-1 {
    width: 24px;
    height: 24px;
    cursor: pointer;
}
</style>