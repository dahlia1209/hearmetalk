import axios from 'axios';
import { AudioDataDto,AudioData } from "@/models/SpeechToText"

export const submitAudio = async (audioData: AudioData): Promise<AudioDataDto> => {
    try {
        // FormDataオブジェクトの作成
        const formData = new FormData();
        // ファイルをFormDataオブジェクトに追加
        formData.append('file', audioData.audioFile);
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/speech_to_text`, formData, {
            withCredentials: true,
        });
        // レスポンスデータの処理
        const responseAudioData = new AudioDataDto(
            // もしbinary_dataがBase64エンコードされた文字列であれば、デコードが必要
            response.data.encoded_data, 
            response.data.duration_ms,
            response.data.filename,
            response.data.mime_type,
            response.data.file_extension,
            response.data.text
        );
        
        return responseAudioData

    } catch (error) {
        console.error('Submit Error:', error);
        throw error;
    }
}

export const submitAudioStreamEmit = async (socket:any,arrayBuffer: ArrayBuffer,chunkCount:number,timeslice:number): Promise<void> => {
    try {
        socket.emit('recording_audio', arrayBuffer,chunkCount,timeslice);
    } catch (error) {
        console.error('Submit Error:', error);
        throw error;
    }
}

export const startRecognitionEmit = (socket:any,fileFormat:string)=>{
    try {
        socket.emit('start_recognition',fileFormat);
    } catch (error) {
        console.error('Submit Error:', error);
        throw error;
    }
}

export const stopRecognitionEmit = (socket:any)=>{
    try {
        socket.emit('stop_recognition');
    } catch (error) {
        console.error('Submit Error:', error);
        throw error;
    }
}
