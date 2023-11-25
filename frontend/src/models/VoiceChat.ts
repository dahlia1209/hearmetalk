export  class AudioType{
    public static mappningList =new Map<string, string>([
        ["audio/webm",".webm"],
        ["audio/webm; codecs=opus",".webm"],
        ["audio/ogg",".ogg"],
        ["audio/ogg; codecs=opus",".ogg"],
        ["audio/ogg; codecs=vorbis",".ogg"],
        ["audio/wav",".wav"],
        ["audio/x-wav",".xwav"],
        ["audio/mp4; codecs=mp4a.40.2 (AAC-LC)",".mp4"],
        ["audio/mp4; codecs=mp4a.40.5 (HE-AAC)",".mp4"],
        ["audio/aac",".aac"],
        ["audio/aacp",".aacp"],
        ["audio/mpeg",".mpeg"],
        ["audio/mp3",".mp3"],
    ]);
}

// public static list = [
//     {mime:"audio/webm",extention:".webm"},
//     {mime:"audio/webm; codecs=opus",extention:".webm"},
//     {mime:"audio/ogg",extention:".ogg"},
//     {mime:"audio/ogg; codecs=opus",extention:".ogg"},
//     {mime:"audio/ogg; codecs=vorbis",extention:".ogg"},
//     {mime:"audio/wav",extention:".wav"},
//     {mime:"audio/x-wav",extention:".xwav"},
//     {mime:"audio/mp4; codecs=mp4a.40.2 (AAC-LC)",extention:".mp4"},
//     {mime:"audio/mp4; codecs=mp4a.40.5 (HE-AAC)",extention:".mp4"},
//     {mime:"audio/aac",extention:".aac"},
//     {mime:"audio/aacp",extention:".aacp"},
//     {mime:"audio/mpeg",extention:".mpeg"},
//     {mime:"audio/mp3",extention:".mp3"},
// ];


// export  class AudioType{
//     public static list = [
//         "audio/webm",
//         "audio/webm; codecs=opus",
//         "audio/ogg",
//         "audio/ogg; codecs=opus",
//         "audio/ogg; codecs=vorbis",
//         "audio/wav",
//         "audio/x-wav",
//         "audio/mp4; codecs=mp4a.40.2 (AAC-LC)",
//         "audio/mp4; codecs=mp4a.40.5 (HE-AAC)",
//         "audio/aac",
//         "audio/aacp",
//         "audio/mpeg",
//         "audio/mp3",
//     ];
// }