import axios from 'axios';
import { Message, ChatCompletionSettings } from "@/models/Chat"
import { AudioDataDto } from "@/models/SpeechToText"
import { AudioData } from "@/models/SpeechToText"

export const submitAudio = async (audioData: AudioData): Promise<AudioDataDto> => {
    try {
        // FormDataオブジェクトの作成
        const formData = new FormData();
        // ファイルをFormDataオブジェクトに追加
        formData.append('file', audioData.audioFile);
        const response = await axios.post(`${process.env.VUE_APP_API_URL}/voice_chat`, formData, {
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