<template>
  <div class="chat-pg-message" v-if="ischatpgessageVisible">
    <div class="chat-message-role" @click="toggleUserRole">
      {{ editableIsUser ? "USER" : "ASSISTANT" }}
    </div>
    <textarea
      class="text-input text-input-md"
      :placeholder="`Enter a ${editableRole} message here.`"
      v-model="editableContent"
      @input="
        updateValue(editableMessageId, editableIsUser, editableRole, editableContent)
      "
    ></textarea>
    <div style="width: 10px">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="none"
        class="chat-message-remove-button"
        width="20"
        height="20"
        @click="removeParent(editableMessageId)"
        role="button"
        tabindex
      >
        <path
          d="M10 16.6667C13.6819 16.6667 16.6667 13.6819 16.6667 10C16.6667 6.31811 13.6819 3.33334 10 3.33334C6.31814 3.33334 3.33337 6.31811 3.33337 10C3.33337 13.6819 6.31814 16.6667 10 16.6667Z"
          stroke="#6E6E80"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        ></path>
        <path
          d="M7.33337 10H12.6667"
          stroke="#6E6E80"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        ></path>
      </svg>
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from "uuid";

export default {
  props: {
    messageId: {
      type: String,
      default: "",
    },
    isUser: {
      type: Boolean,
      default: true,
    },
    content: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      editableMessageId: this.messageId =="" ? uuidv4() :this.messageId,
      editableIsUser: this.isUser,
      editableContent: this.content,
      editableRole: this.isUser ? "user" : "assistant",
      ischatpgessageVisible: true,
    };
  },
  mounted() {
    this.updateValue(this.editableMessageId, this.editableIsUser, this.editableRole, this.editableContent);
  },
  methods: {
    removeParent(messageId) {
      this.ischatpgessageVisible = false;
      this.$emit("delete:message", {messageId});
    },
    toggleUserRole() {
      this.editableIsUser = !this.editableIsUser;
      this.editableRole = this.editableIsUser ? "user" : "assistant";
    },
    updateValue(messageId, isUser, role, content) {
      this.$emit("update:message", { messageId, isUser, role, content });
    },
  },
};
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
