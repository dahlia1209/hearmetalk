<template>
    <div class="voice-chat-view">
        <SettingsArea @settings-upadated="settingsUpdate($event)" :is-speech-enabled="true"/>
        <PromptInputArea :settings="isSpeechEnabled" />
    </div>

</template>
<script setup lang="ts">
import PromptInputArea from "@/components/VoiceChat/PromptInputArea.vue";
import SettingsArea from "@/components/VoiceChat/SettingsArea.vue";
import { ref } from 'vue';

const isSpeechEnabled =ref(true)

function settingsUpdate(updatedIsSpeechEnabled:boolean){
    isSpeechEnabled.value=updatedIsSpeechEnabled
    console.log("settingsUpdate")
    console.log(isSpeechEnabled.value)
}
</script>

<style>
.voice-chat-view{
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 8px;
}

</style>