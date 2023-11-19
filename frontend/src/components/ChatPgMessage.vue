<template>
  <div class="chat-pg-message" v-if="ischatpgessageVisible">
    <div class="chat-message-role" @click="toggleUserRole">
      {{ localMessage.isUser ? "USER" : "ASSISTANT" }}
    </div>
    <textarea class="text-input text-input-md" :placeholder="`Enter a ${localMessage.role} message here.`"
      v-model="localMessage.content" @input="
        updateValue(localMessage)
      "></textarea>
    <div style="width: 10px">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="none" class="chat-message-remove-button"
        width="20" height="20" @click="removeParent(localMessage)" role="button">
        <path
          d="M10 16.6667C13.6819 16.6667 16.6667 13.6819 16.6667 10C16.6667 6.31811 13.6819 3.33334 10 3.33334C6.31814 3.33334 3.33337 6.31811 3.33337 10C3.33337 13.6819 6.31814 16.6667 10 16.6667Z"
          stroke="#6E6E80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
        <path d="M7.33337 10H12.6667" stroke="#6E6E80" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        </path>
      </svg>
    </div>
  </div>
</template>

<script lang="ts">
import { v4 as uuidv4 } from "uuid";
import { defineComponent } from 'vue';
import { Message } from "@/models/Chat"

export default defineComponent({
  props: {
    message: { type: Message, default: () => new Message(uuidv4()) },
  },
  data() {
    return {
      ischatpgessageVisible: true,
      localMessage: this.message
    };
  },
  mounted() {
    //  this.localMessage = new Message(this.message.messageId, this.message.isUser, this.message.content, this.message.role);
    this.updateValue(this.message);
  },
  methods: {
    removeParent(message: Message) {
      this.ischatpgessageVisible = false;
      this.$emit("delete:message", { messageId: message.messageId });
    },
    toggleUserRole() {
      this.localMessage.isUser = !this.localMessage.isUser;
      this.localMessage.role = this.localMessage.isUser ? "user" : "assistant";
    },
    updateValue(message: Message) {
      this.localMessage.messageId = message.messageId;
      this.localMessage.isUser = message.isUser;
      this.localMessage.content = message.content;
      this.localMessage.role = message.role;
      this.$emit("update:message", { message });
    },
  },
});
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

.text-input.text-input-md {
  outline: none;
  resize: none;
  border: none;
  background-color: transparent;
  padding: 12px;
  width: 100%;
  cursor: pointer;
}

.text-input.text-input-md:focus {
  border: 1px solid #19c37d;
  border-radius: 10px;
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
