import { Message, ChatCompletionSettings, MessageDto } from "@/models/Chat"

export class ChatSocket {
    public responseMessages: string[] = []
    public ws: WebSocket | null
    public isConnet: boolean
    private timeoutId: any;

    constructor() {
        this.responseMessages = []
        this.ws = null;
        this.isConnet = false
    }

    send(chatCompletionSettings: ChatCompletionSettings) {
        this.responseMessages = []
        this.ws = new WebSocket(`${import.meta.env.VITE_SOCKET_URL}/chat`);
        this.isConnet = false

        this.ws.onopen = () => {
            this.isConnet = true
            this.ws?.send(JSON.stringify(chatCompletionSettings));
            this.setupTimeout()
        }
        this.ws.onmessage = (event: MessageEvent) => {
            this.responseMessages.push(event.data);
            // console.log(event.data)
            this.setupTimeout()
        };
        this.ws.onerror = (event: Event) => {
            console.error('WebSocket error:', event);
            this.isConnet = false
        };

        this.ws.onclose = (event: CloseEvent) => {
            console.log('WebSocket connection closed:', event);
            this.isConnet = false
        };
    }

    close() {
        if (this.ws) {
            this.ws.close()
        }
    }

    setupTimeout() {
        // // 既存のタイムアウトをクリア
        // clearTimeout(this.timeoutId);

        // // 10秒後に接続を閉じるタイムアウトを設定
        // this.timeoutId = setTimeout(() => {
        //     console.log('10秒間メッセージを受信しなかったため、接続を閉じます。');
        //     this.ws?.close();
        // }, 5000);
    }
}
