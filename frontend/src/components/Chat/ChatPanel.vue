<template>
  <div class="chat-panel">
    <div ref="chatPgExchange" class="chat-pg-exchange">
      <chat-pg-message v-for="message in messages" :key="message.messageId" :message="message"
        @update-message="updateMessages($event); $emit('updateMessages', messages);"
        @delete-message="deleteMessage($event)"></chat-pg-message>
      <button class="chat-pg-message add-message" @click="addMessage()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="none" class="icon" width="20" height="20">
          <path
            d="M10 16.6667C13.6819 16.6667 16.6667 13.6819 16.6667 9.99999C16.6667 6.3181 13.6819 3.33333 10 3.33333C6.31814 3.33333 3.33337 6.3181 3.33337 9.99999C3.33337 13.6819 6.31814 16.6667 10 16.6667Z"
            stroke="#353740" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
          <path d="M10 7.33333V12.6667" stroke="#353740" stroke-width="1.5" stroke-linecap="round"
            stroke-linejoin="round"></path>
          <path d="M7.33337 10H12.6667" stroke="#353740" stroke-width="1.5" stroke-linecap="round"
            stroke-linejoin="round"></path>
        </svg>
        <div class="chat-pg-message add-message">
          <span class="text">Add message</span>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import ChatPgMessage from "@/components/Chat/ChatPgMessage.vue";
import { Message } from "@/models/Chat"
import { v4 as uuidv4 } from "uuid";
import { ref,  watch } from 'vue';

const messages = ref([new Message(uuidv4())])
const chatPgExchange = ref<HTMLInputElement | null>(null)

watch(messages.value, () => {
  if (chatPgExchange.value) {
    chatPgExchange.value.scrollTop = chatPgExchange.value?.scrollHeight;
  }
}, { flush: 'post' })

function addMessage(message: Message = new Message()) {
  message.messageId = uuidv4()
  message.role =
    messages.value.length == 0 ||
      messages.value[messages.value.length - 1].role === "assistant" ? "user" : "assistant";
  messages.value.push(message);
}
function updateMessages(updatedMessage: Message) {
  let message = messages.value.find((m) => m.messageId === updatedMessage.messageId);
  if (message) {
    message = updatedMessage;
  }
}
function deleteMessage(deletedMessage: Message) {
  messages.value = messages.value.filter((m) => m.messageId !== deletedMessage.messageId);
}
defineExpose({
  addMessage
});
</script>

<style scoped>
.chat-pg-message.add-message {
  display: flex;
  align-items: center;
  padding: 12px 18px;
  gap: 12px;
  cursor: pointer;
  background: transparent;
  border: none;
}

.chat-pg-exchange {
  display: flex;
  flex-direction: column;
  overflow: auto;
  height: 500px;
}

.chat-pg-footer {
  display: flex;
}

.btn-submit {
  padding: 5px 12px 7px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  background-color: #10a37f;
  position: relative;
  display: inline-block;
  color: #fff;
}

.btn-submit:hover {
  background-color: #1a7f64;
}

.btn-submit .tooltiptext {
  visibility: hidden;
  width: auto;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 5px;
}

.btn-submit:hover .tooltiptext {
  visibility: visible;
}
</style>
