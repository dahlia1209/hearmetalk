import axios from 'axios';
import { Message, ChatCompletionSettings } from "@/models/Chat"

export const submitChat = async (chatCompletionSettings: ChatCompletionSettings): Promise<Message>=> {
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