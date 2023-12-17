import axios from 'axios';
import { Message, ChatCompletionSettings } from "@/models/Chat"

export const submitChat = async (chatCompletionSettings: ChatCompletionSettings): Promise<Message> => {
    try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/stateless_chat`, chatCompletionSettings, {
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        // レスポンスデータの処理
        const responseMessage = new Message("", response.data.content, response.data.assistant);
        return responseMessage
    } catch (error) {
        console.error('Submit Error:', error);
        throw error;
    }
}

export async function* submitChatStream(chatCompletionSettings: ChatCompletionSettings): AsyncGenerator<string, void, undefined> {
    try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/stateless_chat_stream`, {
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
