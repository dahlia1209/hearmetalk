<template>
  <div class="chat-pg-message" v-if="ischatpgessageVisible">
    <div class="chat-message-role" @click="toggleUserRole">
      {{ localMessage.role === "user" ? "USER" : "ASSISTANT" }}
    </div>
    <textarea class="chat-message-textarea" :placeholder="`Enter a ${localMessage.role} message here.`"
      v-model="localMessage.content" rows="1" @input="
        $emit('updateMessage', localMessage); textareaRef===null?null:resize(textareaRef);
                                                                                              " ref="textareaRef"></textarea>
    <div style="width: 10px">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="none" class="chat-message-remove-button"
        width="20" height="20" @click="deleteMessage" role="button"
        @input="$emit('deleteMessage', { messageId: localMessage.messageId })">
        <path
          d="M10 16.6667C13.6819 16.6667 16.6667 13.6819 16.6667 10C16.6667 6.31811 13.6819 3.33334 10 3.33334C6.31814 3.33334 3.33337 6.31811 3.33337 10C3.33337 13.6819 6.31814 16.6667 10 16.6667Z"
          stroke="#6E6E80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
        <path d="M7.33337 10H12.6667" stroke="#6E6E80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        </path>
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { v4 as uuidv4 } from "uuid";
import { onMounted, ref, withDefaults, } from 'vue';
import { Message } from "@/models/Chat"

export interface Props {
  message?: Message
};
const props = withDefaults(defineProps<Props>(), {
  message: () => new Message(uuidv4())
})

onMounted(() => {
  if (textareaRef.value) {
    resize(textareaRef.value)
  }
})

const localMessage = ref(props.message);
const ischatpgessageVisible = ref(true)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

function resize(textarea: HTMLTextAreaElement) {
  textarea.style.height = 'auto';
  textarea.style.height = (textarea.scrollHeight) + 'px';
};
function deleteMessage() {
  ischatpgessageVisible.value = !ischatpgessageVisible.value;
}
function toggleUserRole() {
  localMessage.value.role = localMessage.value.role === "user" ? "assistant" : "user";
}
</script>

<style scoped>
.chat-pg-message {
  display: flex;
  align-items: center;
  padding: 12px 18px;
  gap: 12px;
  cursor: pointer;

}

.chat-pg-message:hover {
  background-color: #eeeeee;
}

.chat-message-textarea {
  outline: none;
  border: 0 #fff;
  background-color: transparent;
  padding: 12px;
  width: 100%;
  cursor: pointer;
  resize: none;
  box-sizing: border-box;
  line-height: 24px;
  font-size: 16px;
}

.chat-message-textarea:focus {
  box-shadow: inset 0 0 0 1px #19c37d;
  border-radius: 8px;
  background-color: white;
  cursor: auto;
}

.chat-pg-message:hover .chat-message-role {
  background-color: #c5c5d2;
}

.chat-message-role {
  border-radius: 5px;
  padding: 8px;
  flex-grow: 0;
  flex-shrink: 0;
  flex-basis: 100px;
  text-align: left;
}

.chat-pg-message:hover .chat-message-remove-button {
  display: block;
}

.chat-message-remove-button {
  display: none;
  opacity: 0.5;
  transition: opacity 0.3s ease;
}

.chat-message-remove-button:hover {
  display: block;
  opacity: 1;
}

.chat-pg-exchange {
  display: flex;
  flex-direction: column;
}
</style>
