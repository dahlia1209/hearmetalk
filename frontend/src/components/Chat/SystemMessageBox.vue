<template>
    <div class="text-input-with-header">
        <div class="text-input-header-subheading subheading">System</div>
        <div class="text-input-header-wrapper">
            <textarea aria-label="Input" class="text-input-header-buffer" placeholder="You are a helpful assistant."
                v-model="localSystemMessage.content" @input="$emit('updateSystemMessage', localSystemMessage)">
                                </textarea>
        </div>
    </div>
</template>
  
<script lang="ts">
import { v4 as uuidv4 } from "uuid";
import { defineComponent } from 'vue';
import { Message } from "@/models/Chat"

export default defineComponent({
    props: {
        systemmessage: { type: Message, default: () => new Message(uuidv4(),"","system") },
    },
    data() {
        return {
            localSystemMessage: this.systemmessage
        };
    },
    methods: {
    }
});
</script>
  
<style scoped>
.text-input-with-header {
    border: 1px solid #ccc;
    border-radius: 10px;
}

.text-input-with-header .subheading {
    padding: 22px 16px 12px;
    text-align: left;
}

.text-input-header-buffer {
    border: none;
    height: 100%;
    overflow: auto;
    padding: 0 18px 10px;
    width: 100%;
    outline: none;
    resize: none;
    box-sizing: border-box;
}
</style>