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

    // いずれstaic に統一したい
    static toFile(encodedData:string,mimeType:string,filename:string): File {
        const binaryString = window.atob(encodedData);
        const len = binaryString.length;
        const bytes = new Uint8Array(new ArrayBuffer(len));
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        console.log("mimeType")
        console.log(mimeType)
        const blob= new Blob([bytes], { type: mimeType });
        const file=new File([blob],filename)
        console.log("file.type")
        console.log(file.type)
        return new File([blob],filename)
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

// export interface AudioDataDtoResponse{
//     encoded_data: string;
//     duration_ms : number;
//     filename: string;
//     mime_type: string;
//     file_extension:string;
//     text:string;
    
//     toFile(): File
// }

// export class AudioDataDtoResponse{
//     encoded_data: string;
//     duration_ms : number;
//     filename: string;
//     mime_type: string;
//     file_extension:string;
//     text:string;

//     constructor(encoded_data: string, duration_ms: number, filename: string, mime_type: string, file_extension: string, text: string) {
//         this.encoded_data = encoded_data;
//         this.duration_ms = duration_ms;
//         this.filename = filename;
//         this.mime_type = mime_type;
//         this.file_extension = file_extension;
//         this.text = text;
//     }

//     toFile(): File {
//         const binaryString = window.atob(this.encoded_data);
//         const len = binaryString.length;
//         const bytes = new Uint8Array(len);
//         for (let i = 0; i < len; i++) {
//             bytes[i] = binaryString.charCodeAt(i);
//         }
//         const blob= new Blob([bytes], { type: this.mime_type });
//         return new File([blob],this.filename)
//     }
// }