import axios from 'axios';
// import { Message, ChatCompletionSettings } from "@/models/Chat"
import * as chatModel from "@/models/Chat"
import * as assistantModel from "@/models/Assistant"
import { ServerEvents } from "@/models/AITalk"

export const submitChat = async (chatCompletionSettings: chatModel.ChatCompletionSettings): Promise<chatModel.Message> => {
    try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/stateless_chat`, chatCompletionSettings, {
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        // レスポンスデータの処理
        const responseMessage = new chatModel.Message("", response.data.content, response.data.assistant);
        return responseMessage
    } catch (error) {
        console.error('Submit Error:', error);
        throw error;
    }
}

export async function* submitChatStream(chatCompletionSettings: chatModel.ChatCompletionSettings): AsyncGenerator<string, void, undefined> {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/chat_stream`, {
            method: 'POST',
            body: JSON.stringify(chatCompletionSettings),
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', 
        });

        if (response.body) {
            const reader = response.body.getReader();

            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    break;
                }
                const chunkAsString = new TextDecoder().decode(value);
                yield chunkAsString; // ここでチャンクを返します
            }
        } else {
            console.error('Response body is null');
        }
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

export async function solveEquation(message:assistantModel.Message){
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/solve_equation`, {
            method: 'POST',
            body: JSON.stringify(message),
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include', 
        });
        console.log(response)
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

export async function submitChatStreamMessage(ws:WebSocket,chatCompletionSettings: chatModel.ChatCompletionSettings): Promise<void> {
    try {
        ws.send(JSON.stringify(chatCompletionSettings));
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
