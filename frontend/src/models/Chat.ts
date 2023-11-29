export class Message {
    public messageId: string;
    public content: string;
    public role: "user" | "assistant" | "system";

    constructor(messageId: string = "",  content: string = "", role: "user" | "assistant" | "system" = "user") {
        this.messageId = messageId;
        this.content = content;
        this.role = role;
    }

    toDto(): MessageDto {
        return new MessageDto(this.role, this.content);
    }

    static fromDto(dto: MessageDto): Message {
        return new Message("",dto.content,dto.role);
    }
}

export class MessageDto {
    public content: string;
    public role: "user" | "assistant" | "system";

    constructor(role: "user" | "assistant" | "system", content: string) {
        this.role = role;
        this.content = content;
    }
}

export class ChatCompletionSettings {
    public model: "gpt-3.5-turbo" | "gpt-4-1106-preview" | "gpt-4";
    public messages: MessageDto[];
    public temperature: number;
    public max_tokens: number;
    public top_p: number;
    public frequency_penalty: number;
    public presence_penalty: number;

    constructor(
        model:  "gpt-3.5-turbo" | "gpt-4-1106-preview" | "gpt-4"="gpt-3.5-turbo",
        messages: MessageDto[]=[],
        temperature: number=1,
        max_tokens: number=256,
        top_p: number=1,
        frequency_penalty: number=0,
        presence_penalty: number=0
    ) {
        this.model = model;
        this.messages = messages;
        this.temperature = temperature;
        this.max_tokens = max_tokens;
        this.top_p = top_p;
        this.frequency_penalty = frequency_penalty;
        this.presence_penalty = presence_penalty;
    }
}