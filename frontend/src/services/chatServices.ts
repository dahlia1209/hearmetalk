import * as chatModel from "@/models/Chat"
import * as assistantModel from "@/models/Assistant"

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
