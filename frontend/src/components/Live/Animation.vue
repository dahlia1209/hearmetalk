<template>
    <div class="div-1" ref="div1">
        <div class="div-2">
            <button @click="playAudio(); selectAnimation('waiting'); startReadMessageProcess(10000);">start</button>
            <button @click="stopAudio(); stopReadMessageProcess();">stop</button>
            <button @click="accessTokenStateRef = 'unverified'; updateAccessToken();">updateAccessToken</button>
            <button @click="handleVoicevoxAudioPlay('ずんだもんなのだ');">voicevox</button>
            <audio class="audio-1" ref="audio1Ref">
                <source src="@/assets/maou_14_shining_star.mp3" type="audio/mp3">
                お使いのブラウザはオーディオタグをサポートしていません。
            </audio>
        </div>
        <video :hidden="selectedAnimationRef !== 'waiting'" ref="video1">
            <source src="@/assets/zundamon_moving.webm" type="video/webm">
        </video>
        <video :hidden="selectedAnimationRef !== 'negative'" ref="video2">
            <source src="@/assets/hiyori_m10.webm" type="video/webm">
        </video>
        <video :hidden="selectedAnimationRef !== 'positive'" ref="video3">
            <source src="@/assets/hiyori_m08.webm" type="video/webm">
        </video>
        <div class="div-3">
            <div class="div-4">
                <div class="div-5">
                    <div class="div-8">
                        <img :src="commentMessageRef ? commentMessageRef.profileImageUrl : cat" />
                        <div class="div-12">
                            <div class="div-11">
                                <div class="div-13"></div>
                            </div>
                        </div>

                    </div>
                    <div class="div-10">
                        <div class="div-7">{{ commentMessageRef ? commentMessageRef.roleDisplay : "名無し" }}</div>
                        <div class="div-6">{{ commentMessageRef ? commentMessageRef.content : "ここにみんなのコメントが表示されるよ！" }}
                        </div>
                    </div>
                </div>

                <div class="div-5">
                    <div class="div-8">
                        <img src="@/assets/puchitomato.png" />
                    </div>
                    <div class="div-10">
                        <div class="div-7">ずんだもん</div>
                        <div class="div-6">{{ replyMessageRef ? replyMessageRef.content : "ここにずんだもんのリプが表示されるよ！" }}</div>
                        <!-- <div class="div-7">桃瀬ひより</div>
                        <div class="div-6">{{ replyMessageRef ? replyMessageRef.content : "ここにひよりのリプが表示されるよ！" }}</div> -->
                    </div>
                </div>

            </div>
            <!-- <div class="div-4">
            </div> -->
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
import cat from "@/assets/cat_illust.png"


const video1 = ref<null | HTMLVideoElement>(null)
const video2 = ref<null | HTMLVideoElement>(null)
const video3 = ref<null | HTMLVideoElement>(null)
const audio1Ref = ref<null | HTMLAudioElement>(null)
type Animation = "waiting" | "positive" | "negative"
const selectedAnimationRef = ref<Animation>("waiting")
const replyMessageRef = ref<chatModel.Message | null>(null)
const commentMessageRef = ref<chatModel.Message | null>(null)
const messages = ref<chatModel.Message[]>([])
const systemmessageRef = ref<chatModel.Message>(new chatModel.Message())
const speechSynthesizerRef = ref<SpeechSynthesizer | null>(null)
const isSpeakingRef = ref(false)
const processRef = ref<NodeJS.Timeout | undefined>()
const processedMessageIdsRef = ref(new Set())
const isReadingMessageRef = ref(false)
const tokenRef = ref<LiveModel.Token>({ access_token: null, expired_time: undefined, expires_in: null })
const liveChatIdRef = ref<undefined | string>(undefined)
const accessTokenStateRef = ref<"unverified" | "verified" | "verifying">("unverified")
const roleDisplayName="ずんだもん"

onMounted(() => {
    systemmessageRef.value = new chatModel.Message();
    systemmessageRef.value.content = "You are a friend named 'ずんだもん,Zundamon'. You reply with the content of daily conversation. You are available in Japanese and English only. If you are asked a question in Japanese, you will respond in Japanese; if you are asked a question in English, you will respond in English.When answering in Japanese, add 'もんだ' at the end of the word."
    // systemmessageRef.value.content = "You are a friend named 'ひより,Hiyori'. You reply with the content of daily conversation. You are available in Japanese and English only. If you are asked a question in Japanese, you will respond in Japanese; if you are asked a question in English, you will respond in English."
    systemmessageRef.value.role = "system"
    systemmessageRef.value.roleDisplay = roleDisplayName

})

onUnmounted(() => {
    if (speechSynthesizerRef.value) {
        speechSynthesizerRef.value.close()
    }
    stopReadMessageProcess()
})

async function handleVoicevoxAudioPlay(text: string, speakerId: number = 1) {
    const soundRowResponse=await liveServices.synthesisVoicevox(text,speakerId)
    const audioBlob = await soundRowResponse.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl); 
    audio.addEventListener('ended', function() {
        // console.log('音声の再生が終了しました！');
        isSpeakingRef.value=false
    });
    audio.play();
}


function selectAnimation(animation: Animation) {
    selectedAnimationRef.value = animation
    playVideo(selectedAnimationRef.value);
}

function playVideo(animation: Animation) {
    if (video1.value !== null && animation === 'waiting') {
        video1.value.loop = true;
        video1.value.play()
    } else if (video2.value !== null && animation === 'negative') {
        video2.value.loop = true;
        video2.value.play()
    } else if (video3.value !== null && animation === 'positive') {
        video3.value.loop = true;
        video3.value.play()
    } else {
        setTimeout(playVideo, 500, animation);
    }
}

function playAudio() {
    if (audio1Ref.value) {
        audio1Ref.value.volume = 0.05
        audio1Ref.value.loop = true;
        audio1Ref.value.play()
    }
}
function stopAudio() {
    if (audio1Ref.value) {
        audio1Ref.value.pause()
    }
}

async function startReadMessageProcess(ms: number) {
    try {
        await updateAccessToken()
        console.log("読み上げを開始します。");
        processRef.value = setInterval(async () => {
            updateAccessTokenState();
            await updateAccessToken();
            responseMessage();
        }, ms);
    } catch (error) {
        console.error("読み上げ処理中にエラーが発生しました:", error);
    }
}

function stopReadMessageProcess() {
    if (processRef.value) {
        clearInterval(processRef.value);
    }
    console.log("読み上げを停止します。")
}

function updateAccessTokenState() {
    if (accessTokenStateRef.value === "verified" && tokenRef.value.expired_time && tokenRef.value.expired_time < new Date()) {
        accessTokenStateRef.value = "unverified"
    }
}

async function updateAccessToken() {
    if (accessTokenStateRef.value === "unverified") {
        accessTokenStateRef.value = "verifying";
        localStorage.removeItem('access_token');
        localStorage.removeItem('expires_in');
        oauthServices.oauthSignIn(import.meta.env.VITE_OAUTH2_REDIRECT_URI);

        const interval = 500;
        while (true) {
            const accessToken = localStorage.getItem('access_token');
            const expiresIn = Number(localStorage.getItem('expires_in'));
            if (accessToken && expiresIn !== 0) {
                const expiredTime = new Date(new Date().getTime() + (expiresIn - 10) * 1000);
                // const expiredTime = new Date(new Date().getTime() + 60 * 1000);
                const token = {
                    access_token: accessToken,
                    expired_time: expiredTime,
                    expires_in: expiresIn
                };
                accessTokenStateRef.value = "verified";
                tokenRef.value = token;
                return
            }
            await new Promise(resolve => setTimeout(resolve, interval));
        }
    }
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
                        const message = LiveChatMessage.snippet.textMessageDetails.messageText;
                        const authorId = LiveChatMessage.authorDetails.channelId
                        const profileImageUrl = LiveChatMessage.authorDetails.profileImageUrl
                        commentMessageRef.value = addMessageToChat(message, "user", LiveChatMessage.authorDetails.displayName, authorId, profileImageUrl)
                        let response = await chatCompletions(message, authorId)
                        const language = await detectLanguage(response)
                        response = language === "en" || language === "ja" ? response : "Sorry, we only support Japanese or English."
                        replyMessageRef.value = authorId !== null ? addMessageToChat(response, "assistant", roleDisplayName, authorId) : addMessageToChat(response, "assistant", roleDisplayName)
                        const speechSynthesizer = language === "en" || language === "ja" ? initSpeechSynthesizer(language) : initSpeechSynthesizer("en")
                        isSpeakingRef.value = true
                        language === "en"?speechServices.textToSpeech(speechSynthesizer, response):handleVoicevoxAudioPlay(response)
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


function addMessageToChat(content: string, role: "user" | "assistant" | "system", roleDisplay: string, authorId: chatModel.Message["authorId"] = undefined, profileImageUrl: chatModel.Message["profileImageUrl"] = undefined): chatModel.Message {
    const message = new chatModel.Message();
    message.content = content;
    message.role = role;
    message.roleDisplay = roleDisplay;
    if (authorId) {
        message.authorId = authorId
    }
    if (profileImageUrl) {
        message.profileImageUrl = profileImageUrl
    }
    messages.value.push(message);
    return message
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
        return contents;
    }
    const messageDtos = createMessageDtos(authorId);
    const chatCompletionSettings = createChatCompletionSettings(messageDtos);
    const contents = await handleStream(chatCompletionSettings);
    return contents
}
</script>

<style scoped>
.div-1 {
    background-image: url('@/assets/School_music_room_night_lights_ON.jpg');
    /* background-image: url('@/assets/LiveScreen01.png'); */
    display: flex;
    flex-direction: column;
    overflow-y: visible;
    width: 100%;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
}

.div-1 video {
    overflow-y: auto;
    position: absolute;
    max-width: 100%;
    max-height: 100%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.div-2 {
    display: flex;
    flex-direction: row;
}

.div-3 {
    display: flex;
    width: 50%;
    height: 100%;
    flex-direction: column;
    /* padding: 100px; */
}

.div-4 {
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: 200px 200px;
    /* opacity: 80%; */


}

.div-5 {
    padding: 8px;
    overflow: hidden;
    font-style: bold;
    display: flex;
    flex-direction: row;
    background-color: white;
    width: 100%;
    /* background-color: white; */

}

.div-5 img {
    height: 50px;
    opacity: 100%;
    /* overflow: auto; */
}


.div-8 {
    display: flex;
    flex-direction: column;
    font-size: 32px;
    font-weight: bold;
}

.div-6 {
    font-size: 24px;
}

.div-7 {
    font-size: 32px;
    font-weight: bold;
}

.div-9 {
    display: flex;
    direction: row;
}

.div-10 {
    display: flex;
    flex-direction: column;
}

.div-11 {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    height: 100%;
    width: 3px;
    padding: 4px 0px;
    /* background-color: grey; */
}

.div-12 {
    position: relative;
    width: 100%;
    height: 100%;
}

.div-13 {
    height: 100%;
    background-color: grey;
    /* 線の色、ここを変更する */
}
</style>