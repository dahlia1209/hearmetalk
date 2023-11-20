<template>
  <div>
    <SystemMessageBox @update-system-message="handleSystemMessagesUpdate($event)"/>
    <chat-panel @update-messages="handleMessagesUpdate($event)" ref="ChatPanel" />
    <div class="chat-pg-footer">
      <form @submit.prevent="submitForm">
        <button class="btn-submit">
          Submit
          <span class="tooltiptext">Ctrl + Enter</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import SystemMessageBox from "@/components/Chat/SystemMessageBox.vue";
import ChatPanel from "@/components/Chat/ChatPanel.vue";
import { DefineComponent, defineComponent } from 'vue';
import { Message,ChatCompletionSettings,MessageDto } from "@/models/Chat"

export default defineComponent({
  components: {
    SystemMessageBox,
    ChatPanel,
  },
  data() {
    return {
      messages: [] as Message[],
      systemmessage: new Message() as Message,
    };
  },
  methods: {
    handleSystemMessagesUpdate(updatedSystemmessage:Message) {
      this.systemmessage = updatedSystemmessage;
      // console.log(this.systemmessage)
    },
    handleMessagesUpdate(updatedMessages:Message[]) {
      this.messages = updatedMessages;
    },
    async submitForm() {

      const messageDtos=this.systemmessage.content==""?
        [...this.messages.map(message => message.toDto())]:
        [this.systemmessage.toDto(),...this.messages.map(message => message.toDto())]
      const chatCompletionSettings=new ChatCompletionSettings("gpt-4",messageDtos);
      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}/stateless_chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(chatCompletionSettings),
          credentials: 'include',
        }); 

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        const responseMessage = new Message("",responseData.content,responseData.assistant);
        (this.$refs.ChatPanel as DefineComponent).addMessage(responseMessage);
        // 成功の処理をここに書く
      } catch (error) {
        console.error('Submit Error:', error);
        // エラー処理をここに書く
      }
    }
  },
});
</script>

<style scoped>
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
}</style>