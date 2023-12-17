<template>
    <div class="voice-chat-view">
        <SettingsArea />
        <PromptInputArea  />
    </div>

</template>
<script setup lang="ts">
import PromptInputArea from "@/components/VoiceChat/PromptInputArea.vue";
import SettingsArea from "@/components/VoiceChat/SettingsArea.vue";
import { ref } from 'vue';

// const isSpeechEnabled =ref(true)
// const settings =ref(new Settings());

// function settingsUpdate(updatedSettings:Settings){
//     settings.value=updatedSettings
//     console.log("settingsUpdate")
//     console.log(settings.value)
// }
</script>

<style>
.voice-chat-view{
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 8px;
}

</style>