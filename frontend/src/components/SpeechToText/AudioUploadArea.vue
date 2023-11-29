<template>
    <div class="audio-upload-area">
        <img src="@/assets/cloudupload.svg" class="img-1" />
        <div class="div-1">オーディオ ファイルをここにドラッグ アンド ドロップするか、</div>
        <div><button type="button" class="button-1" @click="input1 !== null ? input1.click() : null">ファイルの参照...</button>
        </div>
        <input type="file" accept="audio/*" class="input-1" ref="input1"
            @change="setAudioDataFromInput() " />
        <div class="div-2">
            <img src="@/assets/MicIcon.svg" class="img-2" @click="handleStartRecording()" v-if="recordingState === 'stop'" />
            <img src="@/assets/StopIcon.svg" class="img-2" @click="handleStopRecording()" v-else-if="recordingState === 'recording'" />
            <img src="@/assets/spinner.svg" class="img-2" v-else-if="recordingState === 'pending'" />
        </div>
        <div>
            <div class="div-3" v-if="recordingState === 'stop'">またはマイクで音声を録音する</div>
            <div class="div-3" v-else-if="recordingState === 'recording'">リスニング</div>
            <div class="div-3" v-else-if="recordingState === 'pending'">処理中です。</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { AudioType,AudioData } from "@/models/SpeechToText"
import {  onMounted, ref } from 'vue';
import { submitAudio } from "@/services/speechToTextServices";

const props = defineProps<{ audioDataList: AudioData[] }>()
const recordingState = ref<"recording" | "stop" | "pending">("stop");
const supportedTypes = ref<string[]>([])
const stream = ref<MediaStream | null>(null);
const mediaRecorder = ref<MediaRecorder | null>(null);
const audioChunks = ref<Blob[]>([]);
const input1 = ref<HTMLInputElement | null>(null);
const uploadedAudioData = ref<AudioData | null>(null);
const emit = defineEmits(['audioDataUploaded'])


onMounted(() => {
    uploadedAudioData.value = new AudioData()
})

async function setAudioDataFromInput(): Promise<boolean> {
    if (input1.value && input1.value.files && input1.value.files.length > 0) {
        recordingState.value = "pending";
        uploadedAudioData.value = new AudioData()
        let inputFile = input1.value.files[0]
        // アップロード済みファイルにファイル名が存在する場合は、名前の末尾に数字を追加
        if (props.audioDataList.some(audioData => audioData.audioFile.name === inputFile.name)) {
            console.log("filenameが存在します。")
            let baseName = inputFile.name.replace(/(.*?)(\.[^.]*$|$)/, `$1`);
            let extension = inputFile.name.replace(/.*(\.[^.]*$|$)/, `$1`);
            let count = 2;
            let tries = 1
            let maxTries = 10
            let newFileName = `${baseName}_${count}${extension}`;
            while (props.audioDataList.some(audioData => audioData.audioFile.name === newFileName) && maxTries >= tries) {
                count++
                tries++
                newFileName = `${inputFile.name}_${count}`
            }
            if (maxTries >= tries) {
                inputFile = new File([inputFile], newFileName)
            } else {
                throw Error;
            }
        }
        console.log(inputFile.name)
        const audioData=new AudioData()
        audioData.audioFile = inputFile
        const response = await submitAudio(audioData);
        audioData.audioFile = response.toFile()
        audioData.durationMs = response.durationMs
        audioData.fileExtension = response.fileExtension
        audioData.filename = response.filename
        audioData.mimeType = response.mimeType
        audioData.text = response.text
        uploadedAudioData.value = audioData;

        uploadedAudioData.value.audioFile = inputFile
        emit('audioDataUploaded', uploadedAudioData.value)
        recordingState.value = "stop";
        return true
    } else {
        return false
    }
}

async function startRecording(): Promise<void> {
    audioChunks.value = [];
    recordingState.value = "pending";
    supportedTypes.value = AudioType.typeList.filter((type) =>
        MediaRecorder.isTypeSupported(type)
    );
    stream.value = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder.value = new MediaRecorder(stream.value)
    mediaRecorder.value.ondataavailable = (event) => {
        audioChunks.value.push(event.data);
    };
    mediaRecorder.value.start();
    recordingState.value = "recording";
};

async function stopRecording(): Promise<AudioData | null> {
    recordingState.value = "pending";
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
    audioData.audioFile = new File([audioBlob], `${formattedDate}.webm`, { type: supportedTypes.value[0] });
    const response = await submitAudio(audioData);
    audioData.audioFile = response.toFile()
    audioData.durationMs = response.durationMs
    audioData.fileExtension = response.fileExtension
    audioData.filename = response.filename
    audioData.mimeType = response.mimeType
    audioData.text = response.text
    uploadedAudioData.value = audioData;

    recordingState.value = "stop";
    return uploadedAudioData.value;
};

async function handleStopRecording() {
    try {
        const result = await stopRecording();
        if (result !== null) {
            emit('audioDataUploaded', uploadedAudioData.value);
        }
    } catch (error) {
        console.error("録音の停止中にエラーが発生しました", error);
    }
}

async function handleStartRecording() {
    await startRecording();
}

function getFormattedDate(): string {
    // 現在の日時を取得
    const now = new Date();

    // 日時を 'yyyyMMdd_hhmmss' 形式に整形
    const yyyy = now.getFullYear();
    const MM = String(now.getMonth() + 1).padStart(2, '0'); // 月は0から始まるため+1する
    const dd = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    return `${yyyy}${MM}${dd}_${hh}${mm}${ss}`;
}


</script>
  
<style scoped>
.audio-upload-area {
    display: flex;
    flex-direction: column;
    background-color: #F3F2F1;
    border-style: dotted;
}

.img-1 {
    height: 36px;
}

.img-2 {
    height: 36px;
    cursor: pointer;
}


.button-1 {
    background-color: transparent;
    border: none;
    cursor: pointer;
    text-decoration: underline;
    color: blue;
}

.input-1 {
    display: none;
}

.cloudupload-icon-wrapper img {
    width: 50px;
    height: 50px;
}

.root-404 {
    font-family: "Segoe UI", "Segoe UI Web (West European)", -apple-system,
        BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif;
    -webkit-font-smoothing: antialiased;
    font-size: inherit;
    font-weight: inherit;
    color: rgb(16, 110, 190);
    outline: none;
    text-decoration: underline;
    background: transparent;
    border: none;
    border-bottom: 1px solid transparent;
    cursor: pointer;
    display: inline;
    margin: 0;
    overflow: inherit;
    padding: 0;
    text-align: left;
    text-overflow: inherit;
    user-select: text;
}

.recording-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
}

.spinner {
    width: 50px;
    height: 50px;
}

.spinner .path {
    stroke: #5652bf;
    stroke-linecap: round;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
        stroke-dasharray: 1, 150;
        stroke-dashoffset: 0;
    }

    50% {
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -35;
    }

    100% {
        transform: rotate(360deg);
        stroke-dasharray: 90, 150;
        stroke-dashoffset: -124;
    }
}
</style>