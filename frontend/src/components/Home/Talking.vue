<template>
    <div class="talking-area">
        <div class="div-1">
            <div class="div-2">
                <img src="@/assets/reala_bustup.webp" alt="プロフィール画像">
            </div>
            <div class="div-3">七夜聖りあら</div>
            <div class="div-7">
                <div class="div-6"
                    v-for="item in [new Menu('talking', 'マイクをオフ', micIconMono), new Menu('videoTalking', 'ビデオ通話を開始', videoIcon)] "
                    :key="item.name" @click="homeState.currentView = item.name"><img :src="item.src">{{
                        item.display }}</div>
            </div>
        </div>
        <button class="hangup-button" @click="homeState.currentView = 'profile'">X</button>
    </div>
</template>

<script setup lang="ts">
import { homeState, type HomeState } from '@/store/homeState'
import micIconMono from "@/assets/MicIconMono.svg"
import videoIcon from "@/assets/VideoIcon.svg"
import * as chatModel from "@/models/Chat"
import * as chatServices from "@/services/chatServices"
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk"
import { onMounted, onUnmounted, ref, onBeforeUnmount,watch } from 'vue';

const messages = ref<chatModel.Message[]>([])
const systemmessage = ref<chatModel.Message>(new chatModel.Message())
const speechRecognizerRef = ref<speechsdk.SpeechRecognizer | null>(null)
const speechSynthesizerRef = ref<speechsdk.SpeechSynthesizer | null>(null)
const isAudioPlaying =ref(false)

watch(isAudioPlaying,()=>{
    if(!isAudioPlaying.value){
        initSpeechSynthesizer()
        handleTalking()
    }
})

onMounted(() => {
    addMessageToChat("You are a friend. You reply in Japanese. You reply with the content of daily conversation.", "system", "system");
    initSpeechRecognizer()
    initSpeechSynthesizer()
    handleTalking()
})

function initSpeechRecognizer(){
    const url = new URL(import.meta.env.VITE_SPEECH_TO_TEXT_CONTAINER_URL)
    const speechConfig=speechsdk.SpeechConfig.fromHost(url)
    speechRecognizerRef.value = new speechsdk.SpeechRecognizer(speechConfig)
}

function initSpeechSynthesizer(){
    const url = new URL(import.meta.env.VITE_TEXT_TO_SPEECH_CONTAINER_URL)
    const speechConfig=speechsdk.SpeechConfig.fromHost(url)
    const player = new speechsdk.SpeakerAudioDestination();
        player.onAudioStart = function(_) {
            isAudioPlaying.value=true
        }
        player.onAudioEnd = function (_) {
            isAudioPlaying.value=false
        };
    const audioConfig  = speechsdk.AudioConfig.fromSpeakerOutput(player);
    speechSynthesizerRef.value = new speechsdk.SpeechSynthesizer(speechConfig,audioConfig);
}

onUnmounted(() => {
    if (speechRecognizerRef.value) {
        
        speechRecognizerRef.value.close()
    }
    if (speechSynthesizerRef.value) {
        speechSynthesizerRef.value.close()
    }
})


class Menu {
    name: HomeState["currentView"];
    display: string;
    src: string;

    constructor(name: HomeState["currentView"], display: string, src: string) {
        this.name = name;
        this.display = display
        this.src = src
    }
}

async function handleTalking() {
    const resultText = await speechToText().then((resultText) => {
        return resultText
    }).catch((error) => {
        console.error(error);
        throw new Error();
    });
    const contents = await chatCompletions(resultText)
    await texttospeech(contents).then(async (result) => {
        console.log('音声を再生します。')
        // await waitSeconds(result.audioDuration) 
    }).catch((error) => {

    })
}

async function speechToText(): Promise<string> {
    return new Promise((resolve, reject) => {
        if (speechRecognizerRef.value) {
            speechRecognizerRef.value.recognizeOnceAsync(
                (result) => {
                    resolve(result.text);
                },
                (error) => {
                    console.log(error);
                    reject(error);
                }
            );
        } else {
            reject("speechRecognizerRef.value is not available");
        }
    });
}


async function chatCompletions(text: string) {
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

function addMessageToChat(content: string, role: "user" | "assistant" | "system", roleDisplay: string): chatModel.Message {
    const message = new chatModel.Message();
    message.content = content;
    message.role = role;
    message.roleDisplay = roleDisplay;
    messages.value.push(message);
    return message
}

async function texttospeech(text: string): Promise<speechsdk.SpeechSynthesisResult> {
    return new Promise((resolve, reject) => {
        if (speechSynthesizerRef.value) {
            speechSynthesizerRef.value.speakTextAsync(
                text,
                result => {
                    if (result.reason === speechsdk.ResultReason.SynthesizingAudioCompleted) {
                        resolve(result);
                    } else {
                        reject(result);
                    }
                    speechSynthesizerRef.value?.close();
                },
                error => {
                    throw new Error(error);
                }
            )
        }
    })
}


</script>

<style scoped>
.talking-area {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.div-1 {
    position: relative;
    padding: 20px;
    overflow: hidden;
}

.div-1::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('@/assets/logo_reala.svg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    filter: blur(10px);
    z-index: -1;
}




.div-2 {
    background-color: #ffffff;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    margin: 20px auto;
    position: relative;
    overflow: hidden;
}

.div-2 img {
    width: 100%;
}

.div-3 {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 24px;
}

.div-4 {
    text-align: center;
    color: black;
    margin: 10px 0;
    font-weight: bold;
}

.div-5 {
    display: flex;
    flex-direction: row;
    padding: 10px 0;
    background-color: #f2f2f2;

}

.div-6 {
    text-align: center;
    color: bla;
    flex-grow: 1;
    font-weight: bold;
    cursor: pointer;
}

.div-6 img {
    width: 24px;
    height: 24px;

}

.div-7 {
    display: flex;
    flex-grow: 1;
}

.hangup-button {
    background-color: red;
    border: none;
    border-radius: 50%;
    padding: 20px;
    color: white;
    font-size: 24px;
    margin-top: 20px;
    align-self: center;
    cursor: pointer;
}
</style>