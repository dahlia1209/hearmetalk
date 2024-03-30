<template>
    <div class="chat-list-area">
        <div class="div-9">
            <div class="div-8"><img src="@/assets/reala_bustup.webp" alt=""></div>
            <div class="div-10">{{ replyContent }}</div>
        </div>
        <div class="div-7">
            <div class="div-1">
                トップチャット
            </div>
            <div class="div-2">
                <div class="div-4" v-for="message in messages">
                    {{ `${message.roleDisplay}:${message.content}` }}
                </div>
                <!-- 他のチャットメッセージを追加 -->
            </div>
            <div class="div-3">
                <textarea class="div-5" placeholder="チャット..." v-model="messageContent"></textarea>
                <div class="div-6" @click="messageContent === '' ? '' : handleReplying(messageContent)"><img
                        src="@/assets/submit.svg" alt=""></div>
            </div>
            <button class="div-6" @click="startReadMessageProcess(5000)">startReadMessageProcess</button>
            <button class="div-6" @click="stopReadMessageProcess">stopReadMessageProcess</button>

        </div>
    </div>
</template>
<script lang="ts" setup>
import { onMounted, ref, onUnmounted, watch } from 'vue';
import * as chatModel from "@/models/Chat"
import * as chatServices from "@/services/chatServices"
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk"
import * as liveServices from "@/services/liveServices"
import * as oauthServices from "@/services/oauthServices"
import * as LiveModel from "@/models/Live"

const messageContent = ref("")
const replyContent = ref("")
const messages = ref<chatModel.Message[]>([])
const systemmessageRef = ref<chatModel.Message>(new chatModel.Message())
const speechSynthesizerRef = ref<speechsdk.SpeechSynthesizer | null>(null)
const isSpeakingRef = ref(false)
const processRef = ref<NodeJS.Timeout | undefined>()
const processedMessageIdsRef = ref(new Set())
const isReadingMessageRef = ref(false)
const tokenRef = ref<LiveModel.Token>({ access_token: null, expired_time:undefined, expires_in:null })
const liveChatIdRef = ref<undefined | string>(undefined)

// watch(isSpeaking, () => {
//     if (!isSpeaking.value) {
//         initSpeechSynthesizer()
//     }
// })

onMounted(() => {
    addMessageToChat("You are a friend. You reply in Japanese. You reply with the content of daily conversation.", "system", "system");
    initSpeechSynthesizer()
})

onUnmounted(() => {
    if (speechSynthesizerRef.value) {
        speechSynthesizerRef.value.close()
    }
    stopReadMessageProcess()
})

function startReadMessageProcess(ms: number) {
    processRef.value = setInterval(() => {
        readMessage()
    }, ms);
    console.log("読み上げを開始します。")
    return processRef.value
}
function stopReadMessageProcess() {
    if (processRef.value) {
        clearInterval(processRef.value);
    }
    console.log("読み上げを停止します。")
}


const readMessage = async () => {
    if (isReadingMessageRef.value || isSpeakingRef.value) {
        return;
    }
    if (!tokenRef.value.access_token || !tokenRef.value.expired_time || tokenRef.value.expired_time < new Date()) {
        tokenRef.value = await waitForGetAccessToken()
        console.log(tokenRef.value)
    }
    if (!liveChatIdRef.value&&tokenRef.value.access_token) {
        liveChatIdRef.value = await liveServices.getLiveChatId(tokenRef.value.access_token)
        console.log("liveChatIdRef.value",liveChatIdRef.value)
    }
    isReadingMessageRef.value = true
    try {
        if (tokenRef.value.access_token && liveChatIdRef.value) {
            const LiveChatMessages = await liveServices.getLatestLiveChat(tokenRef.value.access_token, liveChatIdRef.value)
            if (LiveChatMessages) {
                for (const LiveChatMessage of LiveChatMessages) {
                    if (!processedMessageIdsRef.value.has(LiveChatMessage.id)) {
                        const speechSynthesizer = initSpeechSynthesizer()
                        isSpeakingRef.value = true
                        texttospeech(speechSynthesizer, LiveChatMessage.snippet.textMessageDetails.messageText)
                        processedMessageIdsRef.value.add(LiveChatMessage.id);
                        addMessageToChat(LiveChatMessage.snippet.textMessageDetails.messageText, "user", "匿名")
                        await waitForSpeechSynthesizerToClose()
                    }
                }
            }
        }
    } catch (error) {
        console.error('Failed to fetch messages:', error);
    } finally {
        isReadingMessageRef.value = false
    }
}

function waitForGetAccessToken() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('expires_in')
    oauthServices.oauthSignIn(import.meta.env.VITE_OAUTH2_REDIRECT_URI)
    return new Promise<LiveModel.Token>((resolve) => {
        const interval = 500;
        const checkClose = setInterval(() => {
            const accessToken = localStorage.getItem('access_token')
            const expiresIn = Number(localStorage.getItem('expires_in'))
            if (accessToken&&expiresIn) {
                clearInterval(checkClose);
                const expiredTime= new Date(new Date().getTime() + expiresIn * 1000);
                const token:LiveModel.Token={access_token:accessToken,expired_time:expiredTime,expires_in:expiresIn}
                resolve(token);
            }
        }, interval);
    });
}

function waitForSpeechSynthesizerToClose() {
    return new Promise<void>((resolve) => {
        const interval = 100;
        const checkClose = setInterval(() => {
            if (!isSpeakingRef.value) {
                clearInterval(checkClose);
                resolve();
            }
        }, interval);
    });
}


async function handleReplying(content: string) {
    const contents = await chatCompletions(content)
    replyContent.value = contents;
    const speechSynthesizer = initSpeechSynthesizer()
    await texttospeech(speechSynthesizer, contents).then(async (result) => {
        console.log('音声を再生します。')
        // await waitSeconds(result.audioDuration) 
    }).catch((error) => {

    })
}

function addMessageToChat(content: string, role: "user" | "assistant" | "system", roleDisplay: string): chatModel.Message {
    const message = new chatModel.Message();
    message.content = content;
    message.role = role;
    message.roleDisplay = roleDisplay;
    messages.value.push(message);
    return message
}

function initSpeechSynthesizer() {
    const url = new URL(import.meta.env.VITE_TEXT_TO_SPEECH_CONTAINER_URL)
    const speechConfig = speechsdk.SpeechConfig.fromHost(url)
    const player = new speechsdk.SpeakerAudioDestination();
    player.onAudioStart = function (_) {
        isSpeakingRef.value = true
    }
    player.onAudioEnd = function (_) {
        isSpeakingRef.value = false
    };
    const audioConfig = speechsdk.AudioConfig.fromSpeakerOutput(player);
    const speechSynthesizer = new speechsdk.SpeechSynthesizer(speechConfig, audioConfig);
    // speechSynthesizerRef.value = new speechsdk.SpeechSynthesizer(speechConfig, audioConfig);
    return speechSynthesizer
}

async function chatCompletions(text: string) {
    function createMessageDtos() {
        return systemmessageRef.value.content == "" ?
            [...messages.value.map(message => message.toDto())] :
            [systemmessageRef.value.toDto(), ...messages.value.map(message => message.toDto())];
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
        addMessageToChat(contents, "assistant", "りあら")
        return contents;
    }

    addMessageToChat(text, "user", "あなた")
    const messageDtos = createMessageDtos();
    const chatCompletionSettings = createChatCompletionSettings(messageDtos);
    const contents = await handleStream(chatCompletionSettings);
    return contents
}

async function texttospeech(speechSynthesizer: speechsdk.SpeechSynthesizer, text: string): Promise<speechsdk.SpeechSynthesisResult> {
    return new Promise((resolve, reject) => {
        if (speechSynthesizer) {
            speechSynthesizer.speakTextAsync(
                text,
                result => {
                    if (result.reason === speechsdk.ResultReason.SynthesizingAudioCompleted) {
                        resolve(result);
                    } else {
                        reject(result);
                    }
                    speechSynthesizer.close();
                },
                error => {
                    speechSynthesizer.close();
                    throw new Error(error);
                }
            )
        }
    })
}


</script>
<style scoped>
.chat-list-area {
    display: flex;
    flex-direction: row;
}



.div-1 {
    background: #FFFFFF;
    /* 背景色 */
    border-bottom: 1px solid #CCCCCC;
    /* 下線 */
    padding: 10px;
    text-align: center;
    font-weight: bold;
}

.div-2 {
    height: 300px;
    /* 任意の高さに */
    overflow-y: scroll;
    /* チャットが多くなったらスクロール */
    background: #F9F9F9;
    /* 背景色 */
    padding: 10px;
    margin-bottom: 10px;
}

.div-4 {
    margin-bottom: 10px;
}

.div-3 {
    display: flex;
    flex-direction: row;
    bottom: 0;
    width: 100%;
    background: #F1F1F1;

}

.div-5 {
    width: 100%;
    padding: 10px;
    border: none;
    border-top: 1px solid #CCCCCC;
    box-sizing: border-box;
    /* ボーダーを含めた幅で計算 */
}

.div-6 {
    cursor: pointer;
}

.div-7 {
    display: flex;
    flex-direction: column;
    ;
    width: 500px;
}

.div-8 {
    background-color: #ffffff;

    width: 300px;
    height: 300px;
    margin: 20px auto;
    position: relative;
    overflow: hidden;
}

.div-8 img {
    width: 100%;
}

.div-9 {
    display: flex;
    flex-direction: column;
    width: 500px;
}
</style>