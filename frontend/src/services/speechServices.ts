import {SpeechSynthesizer,SpeechSynthesisResult,ResultReason} from "microsoft-cognitiveservices-speech-sdk"
import { TextAnalysisClient, AzureKeyCredential } from "@azure/ai-language-text"

export async function textToSpeech(speechSynthesizer: SpeechSynthesizer, text: string): Promise<SpeechSynthesisResult> {
    return new Promise((resolve, reject) => {
        if (speechSynthesizer) {
            speechSynthesizer.speakTextAsync(
                text,
                result => {
                    if (result.reason === ResultReason.SynthesizingAudioCompleted) {
                        speechSynthesizer.close();
                        resolve(result);
                    } else {
                        speechSynthesizer.close();
                        reject(result);
                    }
                },
                error => {
                    speechSynthesizer.close();
                    throw new Error(error);
                }
            )
        }
    })
}

// export async function textToSpeechWithAutoDetectionLanguage(speechSynthesizer: speechsdk.SpeechSynthesizer, text: string): Promise<speechsdk.SpeechSynthesisResult> {
//     const detectLanguage = async (text: string) => {
//         const client = new TextAnalysisClient(import.meta.env.VITE_TEXTANALYTICS_ENDPOINT, new AzureKeyCredential(import.meta.env.VITE_TEXTANALYTICS_KEY));
//         const result = await client.analyze("LanguageDetection", [text]);
//         if (!result[0]) {
//             return undefined
//         }
//         if (result[0].error) {
//             return undefined
//         }
//         return result[0].primaryLanguage.iso6391Name
//     }

//     function escapeXml(unsafe: string) {
//         return unsafe.replace(/[<>&'"]/g, function (c) {
//             switch (c) {
//                 case '<': return '&lt;';
//                 case '>': return '&gt;';
//                 case '&': return '&amp;';
//                 case '\'': return '&apos;';
//                 case '"': return '&quot;';
//                 default: return c;
//             }
//         });
//     }
//     async function createSsml(text: string) {
//         const escapedText = escapeXml(text);
//         const language = await detectLanguage(text)

//         const xmlString = `<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
//             <voice name="en-US-JennyMultilingualNeural">
//                     <lang xml:lang="${language}">
//                         ${escapedText}
//                     </lang>
//                 </voice>
//             </speak>`;
//         return xmlString
//     }

//     const ssml=await createSsml(text)
//     console.log("ssml",ssml)
//     return new Promise((resolve, reject) => {
//         if (speechSynthesizer) {
//             speechSynthesizer.speakSsmlAsync(
//                 ssml,
//                 result => {
//                     if (result.reason === speechsdk.ResultReason.SynthesizingAudioCompleted) {
//                         speechSynthesizer.close();
//                         resolve(result);
//                     } else {
//                         speechSynthesizer.close();
//                         reject(result);
//                     }
//                 },
//                 error => {
//                     speechSynthesizer.close();
//                     throw new Error(error);
//                 }
//             )
//         }
//     })
// }

