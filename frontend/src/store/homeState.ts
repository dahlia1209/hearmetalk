import { reactive } from 'vue'

export interface HomeState {
  currentView: "profile" | "talking"|"videoTalking"|"chat"
}

export const homeState:HomeState = reactive({
  count: 0,
  increment() {
    this.count++
  },
  currentView:"profile"
})