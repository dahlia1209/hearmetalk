import { v4 as uuidv4 } from 'uuid';

export class MimeTypeMapper {
    static mapping: { [mimeType: string]: string } = {
        "audio/webm":".webm",
        "audio/webm; codecs=opus":".webm",
        "audio/ogg":".ogg",
        "audio/ogg; codecs=opus":".ogg",
        "audio/ogg; codecs=vorbis":".ogg",
        "audio/wav":".wav",
        "audio/x-wav":".x-wav",
        "audio/mp4; codecs=mp4a.40.2 (AAC-LC)":".mp4",
        "audio/mp4; codecs=mp4a.40.5 (HE-AAC)":".mp4",
        "audio/aac":".aac",
        "audio/aacp":".aacp",
        "audio/mpeg":".mpeg",
        "audio/mp3":".mp3",
    };

    static getExtension(mimeType: string): string | null {
        return this.mapping[mimeType] || null;
    }

    static getMimeType(extension: string): string | null {
        const pair = Object.entries(this.mapping).find(([_, ext]) => ext === extension);
        return pair ? pair[0] : null;
    }
}


export class AudioDataDto {
    encodedData: string;
    durationMs: number;
    filename: string;
    mimeType: string;
    fileExtension: string;
    text: string;

    constructor(binaryData: string, durationMs: number, filename: string, mimeType: string, fileExtension: string, text: string = "") {
        this.encodedData = binaryData;
        this.durationMs = durationMs;
        this.filename = filename;
        this.mimeType = mimeType;
        this.fileExtension = fileExtension;
        this.text = text;
    }

    toFile(): File {
        const binaryString = window.atob(this.encodedData);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        const blob= new Blob([bytes], { type: this.mimeType });
        return new File([blob],this.filename)
    }

    toAudioData(): AudioData {
        const audioFile = this.toFile(); // AudioDataDtoのtoFileメソッドを使用してFileオブジェクトを取得
        return new AudioData(
            uuidv4(),
            audioFile, 
            this.durationMs, 
            this.filename, 
            this.mimeType, 
            this.fileExtension, 
            this.text
        );
    }
}

export class AudioData {
    audioDataId:string;
    audioFile: File;
    durationMs: number;
    filename: string;
    mimeType: string;
    fileExtension: string;
    text: string;

    constructor(audioDataId=uuidv4(),audioFile: File=new File([],""), durationMs: number=0, filename: string="", mimeType: string="", fileExtension: string="", text: string = "") {
        this.audioDataId=audioDataId;
        this.audioFile = audioFile;
        this.durationMs = durationMs;
        this.filename = filename;
        this.mimeType = mimeType;
        this.fileExtension = fileExtension;
        this.text = text;
    }

}
