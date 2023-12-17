export class Settings {
    public isSpeechEnabled:boolean;
    public stream:boolean;

    constructor(isSpeechEnabled:boolean=true,stream:boolean=true){
        this.isSpeechEnabled=isSpeechEnabled;
        this.stream=stream
    }
}