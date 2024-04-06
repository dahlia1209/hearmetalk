import { reactive } from 'vue'

export interface LiveState {
    currentView: "animation" | "chatList"
}

export const liveState: LiveState = reactive({
    currentView: "animation"
})