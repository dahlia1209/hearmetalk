<template>
  <div class="chat-area">
    <SystemMessageBox @update-system-message="systemMessageUpdate($event)" />
    <chat-panel @update-messages="messagesUpdate($event)" ref="chatPanel" />
    <div class="chat-pg-footer">
      <form @submit.prevent="submitForm">
        <button class="btn-submit">
          <div v-if="!isSubmitting">Submit
            <span class="tooltiptext">Ctrl + Enter</span>
          </div>
          <div v-else><img src="@/assets/spinner.svg" alt="spinner" class="svg-1" /></div>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import SystemMessageBox from "@/components/Chat/SystemMessageBox.vue";
import ChatPanel from "@/components/Chat/ChatPanel.vue";
import { type DefineComponent, ref } from 'vue';
import { Message, ChatCompletionSettings, MessageDto } from "@/models/Chat"
import { submitChat } from "@/services/chatServices"

const isSubmitting = ref(false)

export interface Props {
  messages?: Message[]
  systemmessage?: Message
};
const props = withDefaults(defineProps<Props>(), {
  messages: () => [],
  systemmessage: () => new Message()
})
const messages = ref(props.messages)
const systemmessage = ref(props.systemmessage)
const chatPanel = ref<DefineComponent | null>(null)

function systemMessageUpdate(updatedSystemmessage: Message) {
  systemmessage.value = updatedSystemmessage;
}
function messagesUpdate(updatedMessages: Message[]) {
  messages.value = updatedMessages;
}
async function submitForm() {
  try {
    isSubmitting.value=true
    const messageDtos = systemmessage.value.content == "" ?
      [...messages.value.map(message => message.toDto())] :
      [systemmessage.value.toDto(), ...messages.value.map(message => message.toDto())]
    const chatCompletionSettings = new ChatCompletionSettings("gpt-4", messageDtos);

    const response = await submitChat(chatCompletionSettings);
    if (chatPanel.value != null) {
      chatPanel.value.addMessage(response);
    }
    isSubmitting.value=false
  } catch (error) {
    console.error('Submit Error:', error);
    isSubmitting.value=false
  }
}

</script>

<style scoped>
.chat-area{
  width: 100%;
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