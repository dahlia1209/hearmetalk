export class Message {
    public role: string;
    public content: string;

    constructor(content: string = "",role: "user" | "assistant" | "system" = "user" ) {
        this.role = role;
        this.content = content;
    }
}