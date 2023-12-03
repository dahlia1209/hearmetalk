import axios from 'axios';
import { AudioDataDto, AudioData } from "@/models/SpeechToText"
import { Speaker } from "@/models/TextToSpeech"
import { getFormattedDate } from "@/utils/dateUtils";

export const submitText = async (audioData: AudioData, speaker: Speaker): Promise<AudioDataDto> => {
    try {
        // DTOへ変換
        const audioDataDto = new AudioDataDto("", 0, "", audioData.mimeType, audioData.fileExtension, audioData.text)

        //リクエスト
        const response = await axios.post<AudioDataDto>(`${import.meta.env.VITE_API_URL}/text_to_speech`, { audioDataDto: audioDataDto, speaker: speaker }, {
            withCredentials: true,
        });        
        // レスポンスデータの処理
        console.log(response)
        const formatedDate=getFormattedDate()
        const filename =`${formatedDate}${response.data.fileExtension}`
        const respnseAudioData = {
            ...audioData,
            audioFile: AudioDataDto.toFile(response.data.encodedData, response.data.mimeType, filename),
            durationMs: response.data.durationMs,
            fileExtension: response.data.fileExtension,
            mimeType: response.data.mimeType,
            filename: filename
        };
        console.info(respnseAudioData);
        return response.data
        // return respnseAudioData

    } catch (error) {
        console.error('Submit Error:', error);
        throw error;
    }
}