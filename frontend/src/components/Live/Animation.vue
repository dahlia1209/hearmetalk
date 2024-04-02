<template>
    <div class="div-1" ref="div1">
        <!-- <video v-if="isSwitchRef" width="320" height="240"  ref="video1" >
            <source src="@/assets/listening.webm" type="video/webm">
        </video>
        <video v-else-if="!isSwitchRef"  width="320" height="240"  ref="video1" >
            <source src="@/assets/speaking.webm" type="video/webm">
        </video> -->

        <button @click="switchMovie()">switch</button>
        <button @click="playVideo()">Play</button>
        <button @click="pauseVideo()">Pause</button>
    </div>
</template>

<script lang="ts" setup>
import { onMounted, ref,watch} from 'vue';



onMounted(()=>{

})
const video1 = ref<null | HTMLVideoElement>(null)
const isSwitchRef=ref(true)


function switchMovie(){
    isSwitchRef.value=!isSwitchRef.value
}

function playVideo() {
    if (video1.value) {
        video1.value.loop=true;
        video1.value.play()
    }
}

function pauseVideo() {
    if (video1.value) {
        video1.value.pause()
    }
}

</script>

<style scoped>
.div-1{
    background-color: aqua;
}
</style>