<template>
    <div class="prompt-input-area">
        <div class="div-6">
            <div class="div-4" v-for="message in messages" :key="message.messageId">
                <img class="img-1" src="@/assets/chatIcon.svg">
                <div class="div-2">
                    <div class="div-3">{{ message.roleDisplay }}</div>
                    <div class="div-5">{{ message.content }}</div>
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
            <button class="button-1" :disabled="!isWaitingForSubmit || !recordingState" @click="handleChatCompletions(textareaInput)"><img
                    src="@/assets/submit.svg"></button>
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
import { submitText } from "@/services/textToSpeechServices";
import { settings } from '@/store/aiChatState'

const textareaRef = ref<HTMLTextAreaElement | null>(null)
const isWaitingForSubmit = ref(true)
const recordingState = ref<"recording" | "stop" | "pending">("stop");
const messages = ref<chatModel.Message[]>([])
const systemmessage = ref<chatModel.Message>(new chatModel.Message())
const textareaInput = ref<string>("")
const errorMessage = ref("")
const selectedSpeaker = ref<Speaker>(Speaker.getSpeaker('Nanami'))
const audioData = ref<AudioData>(new AudioData())
const audioPlayerRef = ref<HTMLAudioElement | null>(null)
const targetMessageRef = ref<chatModel.Message | null>(null)
const speechRecognizerRef = ref<speechsdk.SpeechRecognizer | null>(null)
const isWaiting = ref(true)

onMounted(()=>{
    addMessageToChat("You are a friend. You reply in Japanese. You reply with the content of daily conversation.", "system", "system");
})

async function handleChatCompletions(text:string) {
    function createMessageDtos() {
        return systemmessage.value.content == "" ?
            [...messages.value.map(message => message.toDto())] :
            [systemmessage.value.toDto(), ...messages.value.map(message => message.toDto())];
    }

    function createChatCompletionSettings(messageDtos: chatModel.MessageDto[]) {
        const chatCompletionSettings = new chatModel.ChatCompletionSettings("gpt-3.5-turbo", messageDtos);
        chatCompletionSettings.stream = settings.value.stream;
        return chatCompletionSettings;
    }
    async function handleStream(chatCompletionSettings: chatModel.ChatCompletionSettings) {
        const contentsArray=[];
        for await (const chunk of chatServices.submitChatStream(chatCompletionSettings)) {
            contentsArray.push(chunk);
        }
        const contents=contentsArray.join("");
        addMessageToChat(contents,"assistant","OpenAI")
        return contents;
    }
    
    addMessageToChat(text,"user","あなた")
    const messageDtos = createMessageDtos();
    const chatCompletionSettings = createChatCompletionSettings(messageDtos);
    const contents=await handleStream(chatCompletionSettings);
    return contents
}

function handleSolveEquation(text:string){
    const message=new assistantModel.Message(text)
    chatServices.solveEquation(message)
}



async function handleSubmitButton() {
    // if (textareaInput === "") {
    //     console.error('メッセージを入力してください');
    //     return;
    // }

    try {
        isWaitingForSubmit.value = false;

        // addMessageToChat(textareaInput, "user", "あなた");

        const messageDtos = createMessageDtos();

        const chatCompletionSettings = createChatCompletionSettings(messageDtos);

        if (settings.value.stream) {
            await handleStream(chatCompletionSettings);
        } else {
            await handleSingleMessage(chatCompletionSettings);
        }
    } catch (error) {
        console.error('Submit Error:', error);
    } finally {
        isWaitingForSubmit.value = true;
    }



    function createMessageDtos() {
        return systemmessage.value.content == "" ?
            [...messages.value.map(message => message.toDto())] :
            [systemmessage.value.toDto(), ...messages.value.map(message => message.toDto())];
    }

    function createChatCompletionSettings(messageDtos: chatModel.MessageDto[]) {
        const chatCompletionSettings = new chatModel.ChatCompletionSettings("gpt-4", messageDtos);
        chatCompletionSettings.stream = settings.value.stream;
        return chatCompletionSettings;
    }

    async function handleStream(chatCompletionSettings: chatModel.ChatCompletionSettings) {
        const message = addMessageToChat("", "assistant", "ChatAI");
        targetMessageRef.value = message
        console.log(chatCompletionSettings)
        for await (const chunk of chatServices.submitChatStream(chatCompletionSettings)) {
            targetMessageRef.value.content += chunk;
        }
        handleSubmitText()
    }

    async function handleSingleMessage(chatCompletionSettings: chatModel.ChatCompletionSettings) {
        const response = await chatServices.submitChat(chatCompletionSettings);
        response.roleDisplay = "ChatAI";
        messages.value.push(response);

        if (settings.value.isSpeechEnabled) {
            console.log("handleSubmitText");
            handleSubmitTextToSpeech(response.content);
        }
    }
}

function addMessageToChat(content: string, role: "user" | "assistant" | "system", roleDisplay: string): chatModel.Message {
    const message = new chatModel.Message();
    message.content = content;
    message.role = role;
    message.roleDisplay = roleDisplay;
    messages.value.push(message);
    return message
}

// async function stopRecording(): Promise<AudioData | null> {
//     await new Promise((resolve, reject) => {
//         if (!mediaRecorder.value) {
//             reject(new Error("MediaRecorder is not initialized"));
//             return;
//         }
//         mediaRecorder.value.onstop = resolve;
//         mediaRecorder.value.stop();
//         mediaRecorder.value.stream.getTracks().forEach((track) => track.stop());
//     });

//     // 録音データを処理
//     const audioData = new AudioData()
//     const audioBlob = new Blob(audioChunks.value, { type: supportedTypes.value[0] });
//     const formattedDate = getFormattedDate();
//     audioData.fileExtension = MimeTypeMapper.getExtension(supportedTypes.value[0]) ?? '';
//     audioData.filename = `${formattedDate}${audioData.fileExtension}`
//     audioData.audioFile = new File([audioBlob], audioData.filename, { type: supportedTypes.value[0] });


//     return uploadedAudioData.value;
// };



async function handleSubmitTextToSpeech(text: string) {
    errorMessage.value = ""
    const supportedTypes = Object.keys(MimeTypeMapper.mapping).filter(mimeType => MediaRecorder.isTypeSupported(mimeType));
    if (selectedSpeaker.value && text && supportedTypes.length > 0 && audioPlayerRef.value) {
        console.log("submitText")
        audioData.value.text = text;
        audioData.value.mimeType = supportedTypes[0];
        audioData.value.fileExtension = MimeTypeMapper.getExtension(audioData.value.mimeType) ?? "";
        const response = await submitText(audioData.value, selectedSpeaker.value)
        audioPlayerRef.value.oncanplaythrough = () => {
            audioPlayerRef.value?.play().then(() => {
                console.log('再生が開始されました');
            }).catch((error) => {
                console.error('再生開始エラー:', error);
            });
        }
        audioPlayerRef.value.src = 'data:audio/mpeg;base64,' + response.encodedData
        audioPlayerRef.value.load()

    } else if (!selectedSpeaker.value) {
        errorMessage.value = "スピーカーを選択して下さい"
    } else if (text === "") {
        errorMessage.value = "テキストを入力してください"
    } else if (supportedTypes.length === 0) {
        errorMessage.value = "このブラウザではサポートされていません"
    } else if (!audioPlayerRef.value) {
        errorMessage.value = "ページを再読み込みして再度試してください"
    }
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
                const contents=await handleChatCompletions(resultText)
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

async function handleSubmitText() {
    isWaiting.value = false
    errorMessage.value = ""
    const supportedTypes = Object.keys(MimeTypeMapper.mapping).filter(mimeType => MediaRecorder.isTypeSupported(mimeType));
    if (selectedSpeaker.value && textareaRef.value && textareaRef.value.value && supportedTypes.length > 0 && audioPlayerRef.value) {
        console.log("submitText")
        audioData.value.text = textareaRef.value.value;
        audioData.value.mimeType = supportedTypes[0];
        audioData.value.fileExtension = MimeTypeMapper.getExtension(audioData.value.mimeType) ?? "";
        const response = await submitText(audioData.value, selectedSpeaker.value)
        audioPlayerRef.value.oncanplaythrough = () => {
            audioPlayerRef.value?.play().then(() => {
                console.log('再生が開始されました');
            }).catch((error) => {
                console.error('再生開始エラー:', error);
            });
        }
        audioPlayerRef.value.src = 'data:audio/mpeg;base64,' + response.encodedData
        audioPlayerRef.value.load()

    } else if (!selectedSpeaker.value) {
        errorMessage.value = "スピーカーを選択して下さい"
    } else if (textareaRef.value && !textareaRef.value.value) {
        errorMessage.value = "テキストを入力してください"
    } else if (supportedTypes.length === 0) {
        errorMessage.value = "このブラウザではサポートされていません"
    } else if (!audioPlayerRef.value) {
        errorMessage.value = "ページを再読み込みして再度試してください"
    }
    isWaiting.value = true
}

</script>

<style scoped>
.prompt-input-area {
    flex: display;
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

.div-6 {
    height: 300px;
    flex-direction: column;
    overflow: auto;
}

.img-1 {
    align-self: center;
    width: 40px;
    height: 40px;
}

.img-2 {
    align-self: center;
    width: 150px;
    height: 150px;
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