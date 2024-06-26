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
            <div class="div-2" ref="div2Ref">
                <div class="div-4" v-for="message in messages">
                    {{ `${message.roleDisplay}:${message.content}` }}
                </div>
                <!-- 他のチャットメッセージを追加 -->
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
import { SpeechConfig, SpeechSynthesizer, SpeakerAudioDestination, AudioConfig } from "microsoft-cognitiveservices-speech-sdk"
import * as liveServices from "@/services/liveServices"
import * as oauthServices from "@/services/oauthServices"
import * as speechServices from "@/services/speechServices"
import * as LiveModel from "@/models/Live"
import { TextAnalysisClient, AzureKeyCredential, type DetectedLanguage } from "@azure/ai-language-text"


const messageContent = ref("")
const replyContent = ref("")
const messages = ref<chatModel.Message[]>([])
const systemmessageRef = ref<chatModel.Message>(new chatModel.Message())
const speechSynthesizerRef = ref<SpeechSynthesizer | null>(null)
const isSpeakingRef = ref(false)
const processRef = ref<NodeJS.Timeout | undefined>()
const processedMessageIdsRef = ref(new Set())
const isReadingMessageRef = ref(false)
const tokenRef = ref<LiveModel.Token>({ access_token: null, expired_time: undefined, expires_in: null })
const liveChatIdRef = ref<undefined | string>(undefined)
const div2Ref = ref<null | HTMLDivElement>(null)
const accessTokenStateRef = ref<"unverified" | "verified" | "verifying">("unverified")

// watch(isSpeaking, () => {
//     if (!isSpeaking.value) {
//         initSpeechSynthesizer()
//     }
// })

onMounted(() => {
    systemmessageRef.value = new chatModel.Message();
    systemmessageRef.value.content = "You are a friend. You reply with the content of daily conversation. You are available in Japanese and English only. If you are asked a question in Japanese, you will respond in Japanese; if you are asked a question in English, you will respond in English."
    systemmessageRef.value.role = "system"
    systemmessageRef.value.roleDisplay = "りあら"
})

onUnmounted(() => {
    if (speechSynthesizerRef.value) {
        speechSynthesizerRef.value.close()
    }
    stopReadMessageProcess()
})

function startReadMessageProcess(ms: number) {
    processRef.value = setInterval(() => {
        if (!accessTokenStateRef.value || !tokenRef.value.expired_time || (accessTokenStateRef.value === "verified" && tokenRef.value.expired_time < new Date)) {
            accessTokenStateRef.value = "unverified";
        }
        if (accessTokenStateRef.value === "verified") {
            responseMessage();
        }
        else if (accessTokenStateRef.value === "unverified") {
            accessTokenStateRef.value = "verifying";
            waitForGetAccessToken().then((newToken) => {
                tokenRef.value = newToken;
                accessTokenStateRef.value = "verified";
                responseMessage();
            });
            return;
        }
        else if (accessTokenStateRef.value === "verifying") {
            return;
        }
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

const responseMessage = async () => {
    if (isReadingMessageRef.value || isSpeakingRef.value) {
        return;
    }
    if (!liveChatIdRef.value && tokenRef.value.access_token) {
        liveChatIdRef.value = await liveServices.getLiveChatId(tokenRef.value.access_token)
    }
    isReadingMessageRef.value = true
    try {
        if (tokenRef.value.access_token && liveChatIdRef.value) {
            const LiveChatMessages = await liveServices.getLatestLiveChat(tokenRef.value.access_token, liveChatIdRef.value)
            if (LiveChatMessages) {
                for (const LiveChatMessage of LiveChatMessages) {
                    if (!processedMessageIdsRef.value.has(LiveChatMessage.id)) {
                        // console.log(LiveChatMessage)
                        const message = LiveChatMessage.snippet.textMessageDetails.messageText;
                        const authorId = LiveChatMessage.authorDetails.channelId
                        addMessageToChat(message, "user", LiveChatMessage.authorDetails.displayName, authorId)
                        scrollToBottom()
                        // const language = await detectLanguage(message)
                        // const response = language === "en" || language === "ja" ? await chatCompletions(message, authorId) : "Sorry, we only support Japanese or English."
                        let response = await chatCompletions(message, authorId)
                        const language = await detectLanguage(response)
                        response = language === "en" || language === "ja" ? response : "Sorry, we only support Japanese or English."
                        replyContent.value = response
                        const speechSynthesizer = language === "en" || language === "ja" ? initSpeechSynthesizer(language) : initSpeechSynthesizer("en")
                        isSpeakingRef.value = true
                        speechServices.textToSpeech(speechSynthesizer, response)
                        processedMessageIdsRef.value.add(LiveChatMessage.id);
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

const detectLanguage = async (text: string) => {
    const client = new TextAnalysisClient(import.meta.env.VITE_TEXTANALYTICS_ENDPOINT, new AzureKeyCredential(import.meta.env.VITE_TEXTANALYTICS_KEY));
    const result = await client.analyze("LanguageDetection", [text]);
    if (!result[0]) {
        return undefined
    }
    if (result[0].error) {
        return undefined
    }
    return result[0].primaryLanguage.iso6391Name
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
            if (accessToken && expiresIn !== 0) {
                clearInterval(checkClose);
                const expiredTime = new Date(new Date().getTime() + expiresIn * 1000);
                const token: LiveModel.Token = { access_token: accessToken, expired_time: expiredTime, expires_in: expiresIn }
                resolve(token);
            }
        }, interval);
    });
}

function waitForSpeechSynthesizerToClose() {
    let count = 0;
    const maxWaitMS = 30000;
    const interval = 100;
    const iterationCount = Math.floor(maxWaitMS / interval);
    return new Promise<void>((resolve) => {
        const checkClose = setInterval(() => {
            count++
            if (!isSpeakingRef.value) {
                clearInterval(checkClose);
                resolve();
            }
            if (count > iterationCount) {
                isSpeakingRef.value = false
                clearInterval(checkClose);
                resolve();
            }
        }, interval);
    });
}


// async function handleReplying(content: string) {
//     const contents = await chatCompletions(content)
//     replyContent.value = contents;
//     const speechSynthesizer = initSpeechSynthesizer()
//     await speechServices.texttospeech(speechSynthesizer, contents).then(async (result) => {
//         console.log('音声を再生します。')
//         // await waitSeconds(result.audioDuration) 
//     }).catch((error) => {

//     })
// }

function addMessageToChat(content: string, role: "user" | "assistant" | "system", roleDisplay: string, authorId: chatModel.Message["authorId"] = undefined): chatModel.Message {
    const message = new chatModel.Message();
    message.content = content;
    message.role = role;
    message.roleDisplay = roleDisplay;
    if (authorId) {
        message.authorId = authorId
    }
    messages.value.push(message);
    return message
}

function scrollToBottom() {
    if (div2Ref.value) {
        div2Ref.value.scrollTop = div2Ref.value.scrollHeight;
    }
}

function initSpeechSynthesizer(language: DetectedLanguage["iso6391Name"]) {
    const url = language === "en" ? new URL(import.meta.env.VITE_TEXT_TO_SPEECH_EN_CONTAINER_URL) : language === "ja" ? new URL(import.meta.env.VITE_TEXT_TO_SPEECH_CONTAINER_URL) : new URL(import.meta.env.VITE_TEXT_TO_SPEECH_EN_CONTAINER_URL)
    const speechConfig = SpeechConfig.fromHost(url)
    const player = new SpeakerAudioDestination();
    player.onAudioStart = function (_) {
        isSpeakingRef.value = true
    }
    player.onAudioEnd = function (_) {
        isSpeakingRef.value = false
    };
    const audioConfig = AudioConfig.fromSpeakerOutput(player);

    const speechSynthesizer = new SpeechSynthesizer(speechConfig, audioConfig)
    return speechSynthesizer
}



async function chatCompletions(text: string, authorId: chatModel.Message["authorId"] = undefined): Promise<string> {
    function createMessageDtos(authorId: chatModel.Message["authorId"] = undefined) {
        if (authorId) {
            const filteredMessages = messages.value.filter(message => message.authorId === authorId);
            const messageDtos = systemmessageRef.value.content == "" ?
                [...filteredMessages.map(message => message.toDto())] :
                [systemmessageRef.value.toDto(), ...filteredMessages.map(message => message.toDto())];
            console.log(messageDtos)
            return messageDtos;
        } else {
            const messageDtos = systemmessageRef.value.content == "" ?
                [...messages.value.map(message => message.toDto())] :
                [systemmessageRef.value.toDto(), ...messages.value.map(message => message.toDto())];
            return messageDtos;
        }
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
        if (authorId) {
            addMessageToChat(contents, "assistant", "りあら", authorId)
            scrollToBottom()
        } else {

            addMessageToChat(contents, "assistant", "りあら")
            scrollToBottom()
        }
        return contents;
    }
    const messageDtos = createMessageDtos(authorId);
    const chatCompletionSettings = createChatCompletionSettings(messageDtos);
    const contents = await handleStream(chatCompletionSettings);
    return contents
}

</script>
<style scoped>
.chat-list-area {
    margin-right: 30px;
    display: flex;
    flex-direction: row;
    width: 100%;
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
    flex: 1;
}

.div-8 {
    background-color: #ffffff;
    width: 400px;
    height: 400px;
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
    flex: 2;
}
</style>