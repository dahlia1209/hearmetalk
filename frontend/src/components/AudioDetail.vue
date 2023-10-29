<template>
  <div class="voice-component">
    <label class="root-247" style="font-weight: 600">テスト結果</label>
    <div class="voice-body">
      <div class="css-287">
        <div style="overflow-x: hidden; max-width: 50%">
          <div>
            <span style="color: rgb(96, 94, 92)">ファイル名:</span
            ><span style="text-overflow: ellipsis; overflow: hidden"
              >20230906_161545.wav</span
            >
          </div>
          <div>
            <span style="color: rgb(96, 94, 92)">カスタム エンドポイント:</span
            ><span style="text-overflow: ellipsis; overflow: hidden"
              >[なし]</span
            >
          </div>
        </div>
        <div>
          <div>
            <span c style="color: rgb(96, 94, 92)">言語:</span
            ><span>日本語 (日本)</span>
          </div>
          <div>
            <span style="color: rgb(96, 94, 92)">語句リスト:</span
            ><span>オフ</span>
          </div>
        </div>
        <div class="css-150">
          <div class="css-288">
            <span style="color: rgb(96, 94, 92)">出力形式:</span
            ><span>詳細</span>
          </div>
        </div>
      </div>
      <div>
        <button @click="playAudio">▶️ Play</button>
        <span>00:00</span>
        <input
          type="range"
          v-model="audioFile.currentTime"
          min="0"
          :max="audioFile.durationInSeconds"
          style="width: 70%;"
        />
        {{ audioFile.duration }}
      </div>
      <div>
        <h2>テキスト</h2>
        <p>JSON</p>
        <p>{{ audioFile.transcript }}</p>
      </div>
      <button @click="downloadJson">📂 Download</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      audioFile: {
        fileName: "20230906_161545.wav",
        transcript: "これになる。",
        language: "日本語 (日本)",
        recognitionMode: "音声認識",
        speakerRole: "キャラ",
        duration: "00:03s",
        durationInSeconds: 3,
        currentTime: 0,
      },
    };
  },
  methods: {
    playAudio() {
      // ここに音声ファイルを再生するロジックを追加
    },
    downloadJson() {
      // ここにJSONファイルをダウンロードするロジックを追加
    },
  },
};
</script>

<style scoped>
.voice-body {
  border: 1px solid #ccc;
  padding: 20px;
  text-align: center;
}

.icon-wrapper img {
  width: 50px;
  height: 50px;
}

.root-404 {
  font-family: "Segoe UI", "Segoe UI Web (West European)", -apple-system,
    BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  font-size: inherit;
  font-weight: inherit;
  color: rgb(16, 110, 190);
  outline: none;
  text-decoration: underline;
  background: transparent;
  border: none;
  border-bottom: 1px solid transparent;
  cursor: pointer;
  display: inline;
  margin: 0;
  overflow: inherit;
  padding: 0;
  text-align: left;
  text-overflow: inherit;
  user-select: text;
}

.recording-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.css-287 {
  display: flex;
  flex-flow: row;
  width: auto;
  height: auto;
  box-sizing: border-box;
  justify-content: space-between;
}

.css-221 {
    display: flex;
    flex-flow: column;
    width: auto;
    height: auto;
    box-sizing: border-box;
    flex-grow: 1;
}

.container-296 {
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
}
</style>