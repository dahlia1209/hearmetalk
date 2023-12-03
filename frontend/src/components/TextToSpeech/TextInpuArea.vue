<template>
    <div class="text-input-area">

        <div class="div-1">
            <span>スピーカー:</span>
            <select class="select-1" v-model="selectedSpeaker">
                <option v-for="speaker in speakers" :value="speaker">{{ speaker.nameDisplay }}</option>
            </select>
        </div>
        <span class="span-3">{{ errorMessage }}</span>
        <textarea class="textarea-1" @input="handleTextInput()" ref="textareaRef"
            placeholder="ここに自身のテキストを入力または貼り付け、[再生] ボタンをクリックして音声を聞きます。"></textarea>
        <span class="span-1">{{ currentInputLength }} / 500 文字</span>
        <div class="div-2">
            <button type="button" class="button-1" @click="handleSubmitText()" v-if="isWaiting">
                <img src="@/assets/rightPointingTriangle.svg" class="img-1">
                <span class="span-2">再生</span>
            </button>
            <img src="@/assets/spinner.svg" class="img-2" v-else>
        </div>
        <audio ref="audioPlayerRef" controls><source :src="audioUrl" type="audio/mpeg"></audio>
    </div>
</template>
  
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { Speaker } from "@/models/TextToSpeech"
import { AudioData, MimeTypeMapper } from "@/models/SpeechToText"
import { submitText } from "@/services/textToSpeechServices";
import pydub_mp3 from "@/assets/pydub_mp3.mp3"

const currentInputLength = ref(0)
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const selectedSpeaker = ref<Speaker>(Speaker.getSpeaker('Nanami'))
const speakers = Speaker.speakers
const errorMessage = ref("")
const audioData = ref<AudioData>(new AudioData())
const audioPlayerRef = ref<HTMLAudioElement | null>(null)
const submitedSpeaker = ref<Speaker>(Speaker.getSpeaker('Nanami'))
const isWaiting = ref(true)
const audioUrl=ref("")

const tempPlayerRef = ref<HTMLAudioElement | null>(null)


function handleTextInput() {
    if (textareaRef.value) {
        if (textareaRef.value.textLength > 500) {
            textareaRef.value.value = textareaRef.value.value.substring(0, 500)
        }
        currentInputLength.value = textareaRef.value.textLength;
    }
}

async function handleSubmitText() {
    isWaiting.value = false
    const supportedTypes = Object.keys(MimeTypeMapper.mapping).filter(mimeType => MediaRecorder.isTypeSupported(mimeType));
    if (selectedSpeaker.value && textareaRef.value && textareaRef.value.value && supportedTypes.length > 0 && audioPlayerRef.value) {
        if (audioData.value.text !== textareaRef.value.value || submitedSpeaker.value !== selectedSpeaker.value) {
            console.log("submitText")
            audioData.value.text = textareaRef.value.value;
            submitedSpeaker.value = selectedSpeaker.value
            audioData.value.mimeType = supportedTypes[0];
            audioData.value.fileExtension = MimeTypeMapper.getExtension(audioData.value.mimeType) ?? "";
            const response = await submitText(audioData.value, submitedSpeaker.value)
            audioPlayerRef.value.oncanplaythrough = () => {
                audioPlayerRef.value?.play().then(() => {
                    console.log('再生が開始されました');
                }).catch((error) => {
                    console.error('再生開始エラー:', error);
                });
            }
            audioPlayerRef.value.src = URL.createObjectURL(response.audioFile);
            audioUrl.value=audioPlayerRef.value.src
            
            console.log(response.text)
            audioPlayerRef.value.load()
            tempPlayerRef.value?.load()
        }else{
            audioPlayerRef.value.oncanplaythrough = () => {
                audioPlayerRef.value?.play().then(() => {
                    console.log('再生が開始されました');
                }).catch((error) => {
                    console.error('再生開始エラー:', error);
                });
            }
            audioPlayerRef.value.load()
        }


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
.text-input-area {
    display: flex;
    flex-direction: column;
    border: 2px solid #CCCCCC;
    padding: 12px;
}

.textarea-1 {
    outline: none;
    background-color: transparent;
    width: 100%;
    resize: none;
    box-sizing: border-box;
    line-height: 24px;
    font-size: 16px;
    height: 200px;
    max-height: 200px;
    border: none;
}

.textarea-1:focus {
    border: 2px solid #0078D4;
}

.span-1 {
    border-bottom: 2px solid #CCCCCC;
}

.span-3 {
    color: red;
    text-align: center;
    margin: 10px 0;
    /* 上下のマージン */
}

.button-1 {
    margin-top: 12px;
    display: flex;
    align-items: center;
    background-color: #0078D4;
    border: none;
    cursor: pointer;
    width: 100px;
}

.img-1 {
    height: 36px;
}

.img-2 {
    height: 36px;
}

.span-2 {
    color: white;
    font-size: 16px;
}

.select-1 {}

.div-1 {
    margin-bottom: 12px;
}

.div-2 {
    display: flex;
    justify-content: center;
}
</style>