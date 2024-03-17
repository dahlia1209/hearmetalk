import { reactive } from "vue";

interface State {
    connected: boolean,
    fooEvents: string[],
    barEvents: string[],
    messages: string[],
    responseMessages: string[],
    reconizedMessages: string[],
    isRecognitionReady:boolean

    initResponseMessages():void
}

export const state: State = reactive({
    connected: false,
    fooEvents: [],
    barEvents: [],
    messages: [],
    responseMessages: [],
    reconizedMessages: [],
    isRecognitionReady:false,
    
    initResponseMessages(){
        this.responseMessages=[]
    }
});

const ws =new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
   state.messages.push(event.data);
};

ws.onerror = (event) => {
    console.error('WebSocket error:', event);
};

ws.onerror = (event) => {
    console.log('WebSocket connection closed:', event);
};