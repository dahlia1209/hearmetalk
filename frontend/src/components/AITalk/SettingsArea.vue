<template>
    <div class="settings-area">
        <label class="label-1">
            <input type="checkbox" hidden v-model="settings.isSpeechEnabled" />
            <span class="span-1"></span>
            音声読み上げ
        </label>
        <label class="label-1">
            <input type="checkbox" hidden v-model="settings.stream" />
            <span class="span-1"></span>
            ストリーミング
        </label>
    </div>
</template>

<script setup lang="ts">
import { settings } from '@/store/aiChatState'

</script>

<style scoped>
.settings-area {
    background-color: transparent;
    display: flex;
    flex-direction: row;
    justify-content: center;
    border-bottom: 1px solid #CCCCCC;
}

.label-1 {
    display: inline-block;
    position: relative;
    padding-left: 25px;
    /* チェックマークのスペース */
    cursor: pointer;
    user-select: none;
}

.label-1 input[type="checkbox"] {
    display: none;
    /* 元のチェックボックスを隠す */
}

.label-1 .span-1 {
    position: absolute;
    top: 0;
    left: 0;
    height: 20px;
    width: 20px;
    background-color: #eee;
    border-radius: 3px;
    /* 角丸スタイル */
}

/* チェックボックスがチェックされたときのスタイル */
.label-1 input:checked~.span-1 {
    background-color: #2196F3;
}

/* チェックマークのアイコンを表示 */
.label-1 .span-1:after {
    content: "";
    position: absolute;
    display: none;
}

/* チェックされたときにアイコンを表示 */
.label-1 input:checked~.span-1:after {
    display: block;
}

.label-1 .span-1:after {
    left: 7px;
    top: 3px;
    width: 6px;
    height: 11px;
    border: solid white;
    border-width: 0 3px 3px 0;
    transform: rotate(45deg);
}
</style>