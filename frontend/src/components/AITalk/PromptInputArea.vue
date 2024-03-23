<template>
    <div class="prompt-input-area">
        <div class="div-6">
            <div class="div-4" v-for="message in messages" :key="message.messageId">
                <img class="img-1" src="@/assets/chatIcon.svg">
                <div class="div-2">
                    <div class="div-3">{{ message.roleDisplay }}</div>
                    <div v-if="message.role !== 'system'" class="div-5">{{ message.content }} </div>
                    <textarea class="textarea-2" v-else v-model="message.content">{{ message.content }}</textarea>
                    
                </div>
            </div>
        </div>
        <audio ref="audioPlayerRef"></audio>
        <div class="div-2">
            <button type="button" class="button-1" :disabled="!isWaitingForSubmit || recordingState !== 'stop'"
                v-if="recordingState === 'stop'" @click="handleStartRecording()"><img class="img-2"
                    src="@/assets/MicIcon.svg" alt="MicIcon"></button>
            <img src="@/assets/spinner.svg" class="img-2" v-else-if="recordingState === 'pending'">
            <img src="@/assets/StopIcon.svg" class="img-2" @click="handleStopRecording()"
                v-else-if="recordingState === 'recording'" />
            <!-- <button type="button" class="button-1" :disabled="!isWaitingForSubmit || recordingState !== 'stop'"
                v-if="recordingState === 'stop'" @click="handleStartRecording()"><img class="img-1"
                    src="@/assets/MicIcon.svg" alt="MicIcon"></button>
            <img src="@/assets/spinner.svg" class="img-1" v-else-if="recordingState === 'pending'">
            <img src="@/assets/StopIcon.svg" class="img-1" @click="handleStopRecording()"
                v-else-if="recordingState === 'recording'" /> -->
        </div>
        または
        <div class="div-1">
            <textarea class="textarea-1" placeholder="メッセージを入力してください" rows="1"
                @input="textareaRef === null ? null : resize(textareaRef)" ref="textareaRef"
                v-model="textareaInput"></textarea>
            <button class="button-1" :disabled="!isWaitingForSubmit || !recordingState"
                @click="handleChatCompletions(textareaInput)"><img src="@/assets/submit.svg"></button>
        </div>
    </div>
</template>
<script setup lang="ts">
import { resize } from "@/utils/htmlElementUtils"
import { onMounted, onUnmounted, ref, watch, watchEffect, withScopeId } from 'vue';
import * as chatModel from "@/models/Chat"
import * as assistantModel from "@/models/Assistant"
import * as chatServices from "@/services/chatServices"
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk";
import { AudioData, MimeTypeMapper } from "@/models/SpeechToText"
import { Speaker } from "@/models/TextToSpeech"
// import { submitText } from "@/services/textToSpeechServices";
// import { settings } from '@/store/aiChatState'

const textareaRef = ref<HTMLTextAreaElement | null>(null)
const isWaitingForSubmit = ref(true)
const recordingState = ref<"recording" | "stop" | "pending">("stop");
const messages = ref<chatModel.Message[]>([])
const systemmessage = ref<chatModel.Message>(new chatModel.Message())
const textareaInput = ref<string>("")
const audioPlayerRef = ref<HTMLAudioElement | null>(null)
const speechRecognizerRef = ref<speechsdk.SpeechRecognizer | null>(null)
const editablemessageId = ref("")

onMounted(() => {
    addMessageToChat("You are a friend. You reply in Japanese. You reply with the content of daily conversation.", "system", "system");
})

async function handleChatCompletions(text: string) {
    function createMessageDtos() {
        return systemmessage.value.content == "" ?
            [...messages.value.map(message => message.toDto())] :
            [systemmessage.value.toDto(), ...messages.value.map(message => message.toDto())];
    }

    function createChatCompletionSettings(messageDtos: chatModel.MessageDto[]) {
        const chatCompletionSettings = new chatModel.ChatCompletionSettings("gpt-3.5-turbo", messageDtos);
        chatCompletionSettings.stream = true;
        return chatCompletionSettings;
    }
    async function handleStream(chatCompletionSettings: chatModel.ChatCompletionSettings) {
        const contentsArray = [];
        for await (const chunk of chatServices.submitChatStream(chatCompletionSettings)) {
            contentsArray.push(chunk);
        }
        const contents = contentsArray.join("");
        addMessageToChat(contents, "assistant", "OpenAI")
        return contents;
    }

    addMessageToChat(text, "user", "あなた")
    const messageDtos = createMessageDtos();
    const chatCompletionSettings = createChatCompletionSettings(messageDtos);
    const contents = await handleStream(chatCompletionSettings);
    return contents
}

function editContent(messageId: string) {
    editablemessageId.value = messageId
}

function addMessageToChat(content: string, role: "user" | "assistant" | "system", roleDisplay: string): chatModel.Message {
    const message = new chatModel.Message();
    message.content = content;
    message.role = role;
    message.roleDisplay = roleDisplay;
    messages.value.push(message);
    return message
}

async function handleStartRecording() {
    recordingState.value = "pending";
    await startRecording();
    recordingState.value = "recording";

    async function startRecording(): Promise<void> {
        const url = new URL(import.meta.env.VITE_SPEECH_TO_TEXT_CONTAINER_URL)
        const speechConfig = speechsdk.SpeechConfig.fromHost(url);
        // targetMessageRef.value = addMessageToChat("", "user", "あなた");
        speechRecognizerRef.value = new speechsdk.SpeechRecognizer(speechConfig)
        speechRecognizerRef.value.recognizing = (s, e) => {
            if (e.result.reason === speechsdk.ResultReason.RecognizingSpeech) {
                const recognizedText = e.result.text
                // if (targetMessageRef.value) {
                //     targetMessageRef.value.content = recognizedText

                // }
            }
        }
        speechRecognizerRef.value.recognized = async (s, e) => {
            if (e.result.reason === speechsdk.ResultReason.RecognizedSpeech) {
                const resultText = e.result.text
                const contents = await handleChatCompletions(resultText)
                handletexttospeech(contents)
            }
        }
        speechRecognizerRef.value.canceled = (s, e) => {
            console.log(e)
        }
        speechRecognizerRef.value.startContinuousRecognitionAsync()
    };

    function convertText(text: string) {
        let spaceRemovedString = text.replace(/ /g, '');
        let convertedString = spaceRemovedString.replace(/\./g, '。');
        return convertedString;
    }
}

async function handletexttospeech(text: string) {
    const url = new URL(import.meta.env.VITE_TEXT_TO_SPEECH_CONTAINER_URL)
    const speechConfig = speechsdk.SpeechConfig.fromHost(url);
    const synthesizer = new speechsdk.SpeechSynthesizer(speechConfig);
    // 音声合成の開始
    synthesizer.speakTextAsync(
        text,
        result => {
            if (result.reason === speechsdk.ResultReason.SynthesizingAudioCompleted) {
                console.log('音声合成完了')
            } else {

                console.log(result.errorDetails)
                console.log('音声合成失敗')
            }
            synthesizer.close();
        },
        error => {
            console.log(error)
            console.log('音声合成失敗')
            synthesizer.close();
        }
    )
}

async function handleStopRecording() {
    try {
        recordingState.value = "pending";
        if (speechRecognizerRef.value) {
            speechRecognizerRef.value.stopContinuousRecognitionAsync()
        }
        recordingState.value = "stop";
    } catch (error) {
        console.error("録音の停止中にエラーが発生しました", error);
        recordingState.value = "stop";
    }
}


</script>

<style scoped>
.prompt-input-area {
    display: flex;
    flex-direction: column;
    text-align: center;
}

.div-1 {
    display: flex;
    border-radius: 8px;
    border: 1px solid #C5C5D2;
}

.div-2 {
    display: flex;
    flex-direction: column;
    flex-grow:1;
}

.div-3 {
    text-align: left;
    font-weight: 600;

}

.div-5 {
    display: flex;
    text-align: left;

}

.div-4 {
    display: flex;
    flex-direction: row;
    padding: 16px 8px;
}

.div-7 {
    align-self: self-start;
    cursor: pointer;
}

.div-6 {
    height: 300px;
    flex-direction: column;
    overflow: auto;
}

.img-1 {
    align-self: top;
    width: 40px;
    height: 40px;
}

.img-2 {
    align-self: center;
    width: 150px;
    height: 150px;
}

.img-3 {
    width: 24px;
    height: 24px;
}

.textarea-1 {
    padding: 14px 48px 14px 55px;
    width: 100%;
    border: none;
    resize: none;
    box-sizing: border-box;
    border: 0 #fff;
    font-size: 16px;
}


.textarea-1:focus {
    outline: none;
}

.textarea-2{
    width: 100%;

}

.button-1 {
    background-color: transparent;
    border: none;
    outline: none;
    cursor: pointer;
}

.button-1:disabled {
    color: grey;
    cursor: not-allowed;
    opacity: 0.5;
}
</style>