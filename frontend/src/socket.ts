import { reactive } from "vue";
import { io } from "socket.io-client";

interface State {
    connected: boolean,
    fooEvents: string[],
    barEvents: string[],
    responseMessages: string[],
    reconizedMessages: string[],
    isRecognitionReady:boolean

    initResponseMessages():void
}

export const state: State = reactive({
    connected: false,
    fooEvents: [],
    barEvents: [],
    responseMessages: [],
    reconizedMessages: [],
    isRecognitionReady:false,
    
    initResponseMessages(){
        this.responseMessages=[]
    }
});

const URL = `${import.meta.env.VITE_API_URL}`

export const socket = io(URL);

socket.on("connect", () => {
    state.connected = true;
});

socket.on("disconnect", () => {
    state.connected = false;
});

socket.on("message", (message) => {
    console.log('received message:'+message)
});

socket.on("foo", (args: string) => {
    state.fooEvents.push(args);
});

socket.on("bar", (args: string) => {
    state.barEvents.push(args);
});

socket.on("response_message", (content: string) => {
    state.responseMessages.push(content);
});

socket.on("is_recognition_ready", (isRecognitionReady: boolean) => {
    state.isRecognitionReady=isRecognitionReady;
    console.log("is_recognition_ready:"+state.isRecognitionReady)
});

socket.on("recognized_message", (content: string) => {
    console.log(content)
    state.reconizedMessages.push(content);
});



