<template>
    <div class="audio-upload-area">
        <img :src="cloudupload" class="img-1" />
        <div class="div-1">オーディオ ファイルをここにドラッグ アンド ドロップするか、</div>
        <div><button type="button" class="button-1" @click="input1 !== null ? input1.click() : null">ファイルの参照...</button>
        </div>
        <input type="file" accept="audio/*" class="input-1" ref="input1"
            @change="setAudioFileFromInput() ? $emit('fileUploaded', uploadedFile) : null" />
        <div class="div-2">
            <img :src="MicIcon" class="img-2" @click="startRecording()" v-if="!isRecording" />
            <img :src="StopIcon" class="img-2"
                @click="stopRecording() !== null ? $emit('fileUploaded', uploadedFile) : null" v-else />
        </div>
        <div>
            <div class="div-3" v-if="!isRecording">またはマイクで音声を録音する</div>
            <div class="div-3" v-else>リスニング</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import cloudupload from "@/assets/cloudupload.svg";
import MicIcon from "@/assets/MicIcon.svg";
import StopIcon from "@/assets/StopIcon.svg";
import listening from "@/assets/listening.svg";
import { AudioType } from "@/models/VoiceChat"
import { DefineComponent, onMounted, ref } from 'vue';
import { newExpression } from "@babel/types";

const props = defineProps<{ audioFiles: File[] }>()
const isRecording = ref(false);
// const supportedTypes = ref<string[]>([])
const stream = ref<MediaStream | null>(null);
const mediaRecorder = ref<MediaRecorder | null>(null);
const audioChunks = ref<Blob[]>([]);
const input1 = ref<HTMLInputElement | null>(null);
const uploadedFile = ref<File | null>(null);
const supportedMimeType = ref<string | null>(null);

onMounted(() => {
    supportedMimeType.value = getSupportedMimeType()
})

function setAudioFileFromInput(): boolean {
    if (input1.value && input1.value.files) {
        console.log(props.audioFiles)
        let inputFile = input1.value.files[0]
        // アップロード済みファイルにファイル名が存在する場合は、名前の末尾に数字を追加
        if (props.audioFiles.some(file => file.name === inputFile.name)) {
            console.log("filenameが存在します。")
            let baseName = inputFile.name.replace(/(.*?)(\.[^.]*$|$)/, `$1`);
            let extension = inputFile.name.replace(/.*(\.[^.]*$|$)/, `$1`);
            let count = 2;
            let tries = 1
            let maxTries = 10
            let newFileName = `${baseName}_${count}${extension}`;
            while (props.audioFiles.some(file => file.name === newFileName) && maxTries >= tries) {
                count++
                tries++
                newFileName = `${inputFile.name}_${count}`
            }
            if (maxTries >= tries) {
                inputFile = new File([inputFile], newFileName)
            } else {
                throw newExpression;
            }
        }
        uploadedFile.value = inputFile
        return true
    } else {
        return false
    }
}


// ブラウザがサポートしている MIME タイプを取得
function getSupportedMimeType(): string | null {
    for (let [mimeType] of AudioType.mappningList) {
        if (MediaRecorder.isTypeSupported(mimeType)) {
            return mimeType;
        }
    }
    return null;
}

// MIME タイプに基づいて拡張子を取得し、ファイル名を生成
function createFileName(mimeType: string): string {
    const extension = AudioType.mappningList.get(mimeType) || '';
    const formattedDate = getFormattedDate(); // 日付をフォーマットする関数
    return `${formattedDate}${extension}`;
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

async function startRecording(): Promise<void> {
    console.log("supportedMimeType.value")
    console.log(supportedMimeType.value)

    if (supportedMimeType.value) {
        isRecording.value = true;
        stream.value = await navigator.mediaDevices.getUserMedia({ audio: true })
        mediaRecorder.value = new MediaRecorder(stream.value)
        mediaRecorder.value.ondataavailable = (event) => {
            audioChunks.value.push(event.data);
        };
        mediaRecorder.value.start();
    } else {
        console.error("サポートされているオーディオタイプが見つかりません。");
        return;
    }
};

async function stopRecording(): Promise<File | null> {
    if (supportedMimeType.value) {
        mediaRecorder.value?.stop()
        mediaRecorder.value?.stream.getTracks().forEach((track) => track.stop());
        const audioBlob = new Blob(audioChunks.value, { type: supportedMimeType.value });
        audioChunks.value = [];
        const fileName = createFileName(supportedMimeType.value);
        uploadedFile.value = new File([audioBlob], fileName);
        isRecording.value = false;
        return uploadedFile.value;
    } else {
        console.error("サポートされているオーディオタイプが見つかりません。");
        return null;
    }
};



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

.div-1 {}

.div-4 {}

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
</style>