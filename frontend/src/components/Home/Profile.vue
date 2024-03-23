<template>
    <div class="profile-area">
        <div class="div-1">
            <div class="div-2">
                <img src="@/assets/reala_bustup.webp" alt="プロフィール画像">
            </div>
            <div class="div-3">七夜聖りあら</div>
            <div class="div-4">"私はここにいるよ"</div>
        </div>
        <div class="div-5">
            <div class="div-6"
                v-for="item in [new Menu('chat','チャット'), new Menu('talking','無料通話'),new Menu('videoTalking','ビデオ通話')] "
                :key="item.name" @click="homeState.currentView=item.name">{{ item.display }}</div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { homeState, type HomeState } from '@/store/homeState'

class Menu {
    name:HomeState["currentView"]
    display:string
    constructor(name:HomeState["currentView"],display:string){
        this.name=name;
        this.display=display
    }
}

</script>

<style scoped>
.profile-area {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;

}

.div-1 {
    background-color: #e9eff1;
    padding: 20px;
    background-image: url('@/assets/logo_reala.svg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;

}

.div-1 img {
    width: 100%;
}


.div-2 {
    background-color: #ffffff;
    border-radius: 50%;
    width: 120px;
    height: 120px;
    margin: 20px auto;
    position: relative;
    overflow: hidden;
}

.div-2 img {
    width: 100%;
}

.div-3 {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 24px;
}

.div-4 {
    text-align: center;
    color: black;
    margin: 10px 0;
    font-weight: bold;
}

.div-5 {
    display: flex;
    flex-direction: row;
    padding: 10px 0;
    background-color: #f2f2f2;

}

.div-6 {
    text-align: center;
    color: #333333;
    flex-grow: 1;
    font-weight: bold;
    cursor: pointer;
}
</style>