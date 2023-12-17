<template>
    <div class="prompt-input-area">
        <div class="div-4" v-for="message in messages" :key="message.messageId">
            <img class="img-1" src="@/assets/chatIcon.svg">
            <div class="div-2">
                <div class="div-3">{{ message.roleDisplay }}</div>
                <div class="div-5">{{ message.content }}</div>
            </div>
        </div>
        <audio ref="audioPlayerRef"></audio>
        <div class="div-2">
            <button type="button" class="button-1" :disabled="!isWaitingForSubmit || recordingState !== 'stop'"
                v-if="recordingState === 'stop'" @click="handleStartRecording()"><img src="@/assets/MicIcon.svg"
                    alt="MicIcon"></button>
            <img src="@/assets/spinner.svg" class="img-2" v-else-if="recordingState === 'pending'">
            <img src="@/assets/StopIcon.svg" class="img-2" @click="handleStopRecording()"
                v-else-if="recordingState === 'recording'" />
        </div>
        または
        <div class="div-1">
            <textarea class="textarea-1" placeholder="メッセージを入力してください" rows="1"
                @input="textareaRef === null ? null : resize(textareaRef)" ref="textareaRef"
                v-model="textareaInput"></textarea>
            <button class="button-1" :disabled="!isWaitingForSubmit || !recordingState"
                @click="handleSubmitButton(textareaInput)"><img src="@/assets/submit.svg"></button>
        </div>
    </div>
</template>
<script setup lang="ts">
import { resize } from "@/utils/htmlElementUtils"
import { onMounted, ref, watch, } from 'vue';
import { Message, ChatCompletionSettings, MessageDto } from "@/models/Chat"
import { submitChat, submitChatStream } from "@/services/chatServices"
import { submitAudio } from "@/services/speechToTextServices";
import { getFormattedDate } from "@/utils/dateUtils";
import { AudioData, MimeTypeMapper } from "@/models/SpeechToText"
import { Speaker } from "@/models/TextToSpeech"
import { submitText } from "@/services/textToSpeechServices";
import { Settings } from "@/models/VoiceChat"

export interface Props {
    settings: Settings
};

const props = withDefaults(defineProps<Props>(), {
    settings: () => new Settings()
})

// const isSpeechEnabled = ref(props.settings)
const settings = ref(props.settings)
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const isWaitingForSubmit = ref(true)
const recordingState = ref<"recording" | "stop" | "pending">("stop");
const messages = ref<Message[]>([])
const systemmessage = ref<Message>(new Message())
const audioChunks = ref<Blob[]>([]);
const supportedTypes = ref<string[]>([])
const stream = ref<MediaStream | null>(null);
const mediaRecorder = ref<MediaRecorder | null>(null);
const uploadedAudioData = ref<AudioData | null>(null);
const textareaInput = ref<string>("")
const errorMessage = ref("")
const selectedSpeaker = ref<Speaker>(Speaker.getSpeaker('Nanami'))
const audioData = ref<AudioData>(new AudioData())
const audioPlayerRef = ref<HTMLAudioElement | null>(null)

watch(props, () => {
    settings.value = props.settings
})


async function handleSubmitButton(textareaInput: string) {
    if (textareaInput === "") {
        console.error('メッセージを入力してください');
        return;
    }

    try {
        isWaitingForSubmit.value = false;

        addMessageToChat(textareaInput, "user", "あなた");
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

    function addMessageToChat(content: string, role: "user" | "assistant" | "system", roleDisplay: string) {
        const message = new Message();
        message.content = content;
        message.role = role;
        message.roleDisplay = roleDisplay;
        messages.value.push(message);
    }
    
    function createMessageDtos() {
        return systemmessage.value.content == "" ?
            [...messages.value.map(message => message.toDto())] :
            [systemmessage.value.toDto(), ...messages.value.map(message => message.toDto())];
    }
    
    function createChatCompletionSettings(messageDtos:MessageDto[]) {
        const chatCompletionSettings = new ChatCompletionSettings("gpt-4", messageDtos);
        chatCompletionSettings.stream = settings.value.stream;
        return chatCompletionSettings;
    }
    
    async function handleStream(chatCompletionSettings:ChatCompletionSettings) {
        addMessageToChat("", "assistant", "ChatAI");
    
        for await (const chunk of submitChatStream(chatCompletionSettings)) {
            messages.value[messages.value.length - 1].content += chunk;
        }
    }
    
    async function handleSingleMessage(chatCompletionSettings:ChatCompletionSettings) {
        const response = await submitChat(chatCompletionSettings);
        response.roleDisplay = "ChatAI";
        messages.value.push(response);
    
        if (settings.value.isSpeechEnabled) {
            console.log("handleSubmitText");
            handleSubmitTextToSpeech(response.content);
        }
    }
}

async function startRecording(): Promise<void> {
    audioChunks.value = [];
    supportedTypes.value = Object.keys(MimeTypeMapper.mapping).filter(mimeType => MediaRecorder.isTypeSupported(mimeType));
    stream.value = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream.value)
    mediaRecorder.value.ondataavailable = (event) => {
        audioChunks.value.push(event.data);
    };
    mediaRecorder.value.start();
    
};

async function stopRecording(): Promise<AudioData | null> {
    await new Promise((resolve, reject) => {
        if (!mediaRecorder.value) {
            reject(new Error("MediaRecorder is not initialized"));
            return;
        }
        mediaRecorder.value.onstop = resolve;
        mediaRecorder.value.stop();
        mediaRecorder.value.stream.getTracks().forEach((track) => track.stop());
    });

    // 録音データを処理
    const audioData = new AudioData()
    const audioBlob = new Blob(audioChunks.value, { type: supportedTypes.value[0] });
    const formattedDate = getFormattedDate();
    audioData.fileExtension = MimeTypeMapper.getExtension(supportedTypes.value[0]) ?? '';
    audioData.filename = `${formattedDate}${audioData.fileExtension}`
    audioData.audioFile = new File([audioBlob], audioData.filename, { type: supportedTypes.value[0] });

    // テキストデータ取得
    const response = await submitAudio(audioData);

    //取得データセット
    audioData.audioFile = response.toFile()
    audioData.durationMs = response.durationMs
    audioData.mimeType = response.mimeType
    audioData.text = response.text
    uploadedAudioData.value = audioData;

    return uploadedAudioData.value;
};

async function handleStopRecording() {
    try {
        recordingState.value = "pending";
        const result = await stopRecording();
        if (result !== null) {
            // emit('audioDataUploaded', uploadedAudioData.value);
            handleSubmitButton(result.text)
        }
        recordingState.value = "stop";
    } catch (error) {
        console.error("録音の停止中にエラーが発生しました", error);
        recordingState.value = "stop";
    }
}

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
    text-align: left;
}

.div-4{
    display: flex;
    flex-direction: row;
    padding: 16px 8px;
}

.img-1{
    align-self: self-start;
}

.textarea-1 {
    padding: 14px 48px 14px 55px;
    width: 100%;
    border: none;
    resize: none;
    box-sizing: border-box;
    border: 0 #fff;
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