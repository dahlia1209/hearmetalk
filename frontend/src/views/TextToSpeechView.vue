<template>
    <div class="text-to-speech">
        <TextInpuArea />

    </div>
</template>

<script setup lang="ts">
import TextInpuArea from "@/components/TextToSpeech/TextInpuArea.vue";


</script>

<style scoped>
.text-to-speech{
    display: flex;
    flex-direction: column;
    width: 100%;
}
</style>