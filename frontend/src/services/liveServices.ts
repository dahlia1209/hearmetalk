
import * as LiveModel from "@/models/Live"

export const getLiveChatId = async (accessToken: string): Promise<string | undefined> => {
    const params = {
        access_token: accessToken,
        part: "id,snippet",
        broadcastStatus: "active"
    };
    const queryString = new URLSearchParams(params).toString();

    try {
        const response = await fetch(`https://www.googleapis.com/youtube/v3/liveBroadcasts?${queryString}`, {
            method: 'get',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data: LiveModel.LiveBroadcasts.LiveBroadcastListResponse = await response.json();

        if (data.items.length === 0) {
            return undefined;
        }

        return data.items[0].snippet.liveChatId;
    } catch (error) {
        console.error('Fetching error:', error);
        return undefined;
    }
};

export const getLatestLiveChat = async (accessToken: string, liveChatId: string): Promise<LiveModel.LiveChatMessages.LiveChatMessage[] | undefined> => {
    if (liveChatId || accessToken) {
        const params = {
            access_token: accessToken,
            liveChatId: liveChatId,
            part: "id,snippet,authorDetails"
        };
        const queryString = new URLSearchParams(params).toString();

        try {
            const response = await fetch(`https://www.googleapis.com/youtube/v3/liveChat/messages?${queryString}`, {
                method: 'get',
                headers: {
                    'Content-Type': 'application/json'
                }
            })

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data: LiveModel.LiveChatMessages.LiveChatMessageListResponse = await response.json();

            if (data.items.length === 0) {
                return undefined;
            }

            return data.items;
        } catch (error) {
            console.error('Fetching error:', error);
            return undefined;
        }
    } else {
        throw new Error('parameters are not defined');
        return undefined;
    }
}

export const synthesisVoicevox=async (text: string, speakerId: number = 1)=> {
    // const text = "私はずんだもんなのだ。よろしくなのだ。"
    const res = await fetch(`https://voicevox.hearmetalk.net/audio_query?text=${text}&speaker=${speakerId}`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        }

    })

    const query = await res.json()

    const soundRowResponse = await fetch(`https://voicevox.hearmetalk.net/synthesis?speaker=${speakerId}&enable_interrogative_upspeak=true`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'audio/wav',
            'responseType': "stream"
        },
        body: JSON.stringify(query)
    })
    if (!soundRowResponse.ok) {
        throw new Error('音声合成に失敗しました');
    }
    return soundRowResponse
}