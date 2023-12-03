export type SpeakerName = 'Nanami' | 'Keita' | 'Aoi' | 'Daichi' | 'Mayu' | 'Naoki' | 'Shiori';

export class Speaker {
    public language: string;
    public languageDisplay: string;
    public sex: string;
    public sexDisplay: string;
    public name:SpeakerName;
    public nameDisplay:string;
    public synthesisVoiceName: string;

    constructor(language: string, sex: string, name: SpeakerName,nameDisplay: string, synthesisVoiceName: string) {
        this.language = language;
        this.languageDisplay = this.languageDisplayFunc(language);
        this.sex = sex;
        this.sexDisplay = this.sexDisplayFunc(sex);
        this.name = name;
        this.nameDisplay = nameDisplay;
        this.synthesisVoiceName = synthesisVoiceName;
    }

    public languageDisplayFunc(language: string): string {
        const languageMap: { [key: string]: string }  = {
            'English': '英語',
            'Japanese': '日本語',
        };
        return languageMap[language] || language;
    }

    public sexDisplayFunc(sex: string): string {
        const sexMap : { [key: string]: string } = {
            'Male': '男性',
            'Female': '女性',
        };
        return sexMap[sex] || sex;
    }

    static getSpeaker(name: SpeakerName): Speaker  {
        const speaker= this.speakers.find(speaker => speaker.name === name);
        return speaker ?? this.speakers[0]
    }

    static speakers: Speaker[] = [
        new Speaker('Japanese','Female', 'Nanami', '七海','ja-JP-NanamiNeural'),
        new Speaker('Japanese','Male', 'Keita', '圭太','ja-JP-KeitaNeural'),
        new Speaker('Japanese','Female', 'Aoi', '碧衣','ja-JP-AoiNeural'),
        new Speaker('Japanese','Male', 'Daichi', '大智','ja-JP-DaichiNeural '),
        new Speaker('Japanese','Female', 'Mayu', '真夕','ja-JP-MayuNeural'),
        new Speaker('Japanese','Male', 'Naoki', '直紀','ja-JP-NaokiNeural'),
        new Speaker('Japanese','Female', 'Shiori', '志織','ja-JP-ShioriNeural'),
    ];
}