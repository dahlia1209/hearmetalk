<template>
    <div class="voice-chat-view">
        <SettingsArea />
        <PromptInputArea  />
        <!-- <button @click="sendMessage">Send Message</button> -->
        <!-- <input type="text" v-model="text" /> -->
    </div>
</template>

<script setup lang="ts">
import PromptInputArea from "@/components/AITalk/PromptInputArea.vue";
import SettingsArea from "@/components/AITalk/SettingsArea.vue";
import { onBeforeUnmount, onMounted, ref ,watch} from 'vue';
// import { state,socket } from "@/socket";



// onBeforeUnmount(() => {
//     console.log("socket.disconnect")
//     socket.disconnect();
// })
// onMounted(() => {
//     console.log("socket.connect")
//     socket.connect()
// })

// function sendMessage() {
//     console.log("sendMessage")
//     const message = 'Hello, server!'; 
//     socket.emit('message', message);
// }  
</script>