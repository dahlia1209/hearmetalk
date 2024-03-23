<template>
    <div class="settings-area">
        <div class="parameter-panel">
            <div class="parameter">
                <label for="model">Model</label>
                <select id="model">
                    <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
                    <option value="gpt-4">gpt-4</option>
                </select>
            </div>
            <div class="parameter">
                <label for="temperature">Temperature</label>
                <input type="number" id="temperature" value="1">
            </div>
            <div class="parameter">
                <label for="max-length">Maximum length</label>
                <input type="number" id="max-length" value="256">
            </div>
            <div class="parameter">
                <label for="stop-sequences">Stop sequences</label>
                <input type="text" id="stop-sequences">
            </div>
            <div class="parameter">
                <label for="top-p">Top P</label>
                <input type="number" id="top-p" value="1">
            </div>
            <div class="parameter">
                <label for="frequency-penalty">Frequency penalty</label>
                <input type="number" id="frequency-penalty" value="0">
            </div>
            <div class="parameter">
                <label for="presence-penalty">Presence penalty</label>
                <input type="number" id="presence-penalty" value="0">
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
// import { settings } from '@/store/aiChatState'

</script>

<style scoped>
.settings-area {
    background-color: transparent;
    display: flex;
    flex-direction: column;
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