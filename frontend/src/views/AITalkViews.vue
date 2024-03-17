<template>
    <div class="voice-chat-view">
        <div class="div-1">
            <PromptInputArea  />
        </div>
        <div class="div-2">
            <SettingsArea />
        </div>
    </div>
</template>

<script setup lang="ts">
import PromptInputArea from "@/components/AITalk/PromptInputArea.vue";
import SettingsArea from "@/components/AITalk/SettingsArea.vue";
import { onBeforeUnmount, onMounted, ref ,watch} from 'vue';

</script>

<style scoped>
.voice-chat-view{
    display: flex;
    flex-direction: row;
}
.div-1{
    flex-grow: 1;
}


.div-2{
    width: 200px; 
}


</style>