<template>
    <div class="voice-chat-view">
        <SettingsArea />
        <PromptInputArea  />
    </div>

</template>
<script setup lang="ts">
import PromptInputArea from "@/components/VoiceChat/PromptInputArea.vue";
import SettingsArea from "@/components/VoiceChat/SettingsArea.vue";

</script>

<style>
.voice-chat-view{
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 8px;
}

</style>