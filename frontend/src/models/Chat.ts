export class Message {
    public messageId: string;
    public isUser: boolean;
    public content: string;
    public role: "user" | "assistant";

    constructor(messageId: string = "", isUser: boolean = true, content: string = "", role: "user" | "assistant" = "user") {
        this.messageId = messageId;
        this.isUser = isUser;
        this.content = content;
        this.role = role;
    }
}