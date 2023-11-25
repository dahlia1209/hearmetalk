<template>
    <div class="audio-file-list">
        <div tabindex="0" class="div-1" v-for="(file, index,) in files" :key="file.name"
            :class="{ 'selected': selectedFileIndex === index }" @click="fileSelected(file, index)">
            <img :src="GreenCheck" alt="GreenCheck">
            <button type="button" class="button-1" @click="fileSelected(file, index);" ref="filesRefs">{{ file.name
            }}</button>
            <img :src="TrashBin" alt="TrashBin" class="svg-1" @click="removeFile(index)">
        </div>
    </div>
</template>

<script setup lang="ts">
import { DefineComponent, defineProps, defineComponent, ref, watch } from 'vue';
import GreenCheck from "@/assets/GreenCheck.svg";
import TrashBin from "@/assets/TrashBin.svg";

const props = defineProps<{ file?: File | null }>()
const files = ref<File[]>([]);
const filesRefs = ref<HTMLElement[]>([]);
const emit = defineEmits(['changedFiles', 'fileSelected'])
const selectedFileIndex = ref<number | null>(null)


watch(props, () => {
    if (props.file) {
        files.value.push(props.file)
    }
    emit('changedFiles', files.value)
})

watch(filesRefs.value, () => {
    if (filesRefs.value.length > 0) {
        filesRefs.value[filesRefs.value.length - 1].click()
    }
})

function fileSelected(file: File, index: number) {
    selectedFileIndex.value = index;
    emit('fileSelected', file)
}

function removeFile(index: number) {
    files.value.splice(index, 1)
}


</script>

<style scoped>
.audio-file-list {
    display: flex;
    flex-direction: column;
    border: 1px;
    border-color: grey;
    border-style: solid;
    max-height: 100px;
    height: 100px;
    overflow: auto;
}



.button-1 {
    background-color: transparent;
    border: none;
    cursor: pointer;
    text-decoration: underline;
    color: blue;
    border-bottom: #EDEBE9;
    border-bottom: 2px solid #F3F2F1;
    font-size: 16px;
}

.div-1 {
    cursor: pointer;
    padding: 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.div-1:hover {
    background-color: #F3F2F1;
}

.svg-1 {
    width: 16px;
    height: 16px;
}



.selected {
    background-color: #F3F2F1;
}
</style>