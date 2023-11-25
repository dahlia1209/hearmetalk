<template>
    <div class="audio-file-Detail">
        <div class="div-1">
            <div >ファイル名：{{ file?.name}}</div>
            <div>言語：</div>
        </div>
        <div class="div-2">
            <img :src="replayButton" alt="replayButton" class="svg-1" @click="playAudio()">
            <audio ref="audioPlayer"></audio>
        </div>
    </div>
</template>

<script setup lang="ts">
import { DefineComponent, defineProps, defineComponent, ref, watch,onMounted } from 'vue';
import replayButton from "@/assets/replayButton.svg";

const props = defineProps<{ file: File | null }>()
const file = ref<File|null>(null);
const audioPlayer=ref<HTMLAudioElement|null>(null)

watch(props, () => {
    if (props.file) {
        file.value = props.file
    }
})

function playAudio(){
    console.log("playAudio")
    console.log(file.value && audioPlayer.value)
    if(file.value && audioPlayer.value){
        const audioUrl = URL.createObjectURL(file.value);
        audioPlayer.value.src=audioUrl;
        audioPlayer.value.play();
    }
}

</script>

<style scoped>
.audio-file-Detail{
    border: 2px solid ;
    flex-direction: column;
    border-color: #605E5C;
    padding: 4px;
}
.div-1{
    display: flex;
    justify-content: space-between; 
}
.div-2{
    display: flex;
    justify-content: space-between; 
}
.svg-1{
    width: 24px;
    height: 24px;
    cursor: pointer;
}
</style>