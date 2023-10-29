<template>
  <div class="css-298">
    <label class="root-299" style="font-size: 0.875rem; font-weight: 600"
      ><span>オーディオ ファイル</span></label
    >
    <div class="file-list css-300">
      <div
        v-for="file in files"
        :key="file.name"
        class="file-item"
        style="
          height: 34px;
          padding: 3px 10px;
          border-bottom: 1px solid rgb(237, 235, 233);
        "
      >
        <div style="width: 16px">
          <img :src="GreenCheck" alt="GreenCheck" class="icon" />
        </div>
        <button
          type="button"
          :title="file.name"
          class="root-413"
          style="
            color: rgb(16, 110, 190);
            max-width: 260px;
            overflow-x: hidden;
            white-space: nowrap;
            background-color: transparent;
            border: none;
            cursor: pointer;
          "
        >
          {{ file.name }}
        </button>

        <span class="file-actions">
          <button
            type="button"
            title="削除"
            class="root-413"
            style="margin-left: 5px 
            background-color: transparent;
            border: none;
            cursor: pointer;"
            @click="deleteFile(file)"
          >
            削除
          </button>
        </span>
      </div>
    </div>
    <button
      type="button"
      class="root-207"
      style="color: rgb(16, 110, 190); align-self: start; padding: 5px 10px"
      @click="deleteAllFiles"
    >
      すべてクリア
    </button>
  </div>
</template>

<script>
import GreenCheck from "@/assets/GreenCheck.svg";
import TrashBin from "@/assets/TrashBin.svg";

export default {
  data() {
    return {
      files: [
        { name: "20230904_211146.wav", checked: true },
        { name: "20230904_211321.wav", checked: false },
        { name: "20230904_211542.wav", checked: true },
        { name: "20230904_211551.wav", checked: true },
      ],
      GreenCheck,
      TrashBin,
    };
  },
  methods: {
    deleteFile(file) {
      // ここにファイルの削除ロジックを書く
      const index = this.files.indexOf(file);
      if (index !== -1) {
        this.files.splice(index, 1);
      }
    },
    deleteAllFiles() {
      this.files = [];
    },
  },
};
</script>
<style scoped>
.file-list {
  padding: 10px;
}
.file-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  flex-flow: row;
  width: auto;
  height: auto;
  box-sizing: border-box;
  justify-content: center;
}
.file-actions {
  margin-left: auto;
}
.css-298 {
  display: flex;
  flex-flow: column;
  width: auto;
  height: 220px;
  box-sizing: border-box;
  margin-top: 20px;
  border-color: rgb(161, 159, 157);
  border-style: solid;
  border-width: 1px;
}

.root-299 {
  font-family: "Segoe UI", "Segoe UI Web (West European)", "Segoe UI",
    -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  font-size: 14px;
  font-weight: 600;
  color: rgb(50, 49, 48);
  box-sizing: border-box;
  box-shadow: none;
  margin: 0px;
  display: block;
  padding: 5px 10px;
  overflow-wrap: break-word;
  border-bottom: 1px solid rgb(237, 235, 233);
}

.css-300 {
  display: flex;
  flex-flow: column;
  width: auto;
  height: auto;
  box-sizing: border-box;
  flex-grow: 1;
  overflow: auto;
}

.css-205 {
  display: flex;
  flex-flow: column;
  width: auto;
  height: auto;
  box-sizing: border-box;
  flex-grow: 1;
}

.root-207 {
  font-family: "Segoe UI", "Segoe UI Web (West European)", "Segoe UI",
    -apple-system, BlinkMacSystemFont, Roboto, "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  font-size: inherit;
  font-weight: inherit;
  color: rgb(0, 120, 212);
  outline: none;
  text-decoration: none;
  background: none transparent;
  border-top: none;
  border-right: none;
  border-left: none;
  border-image: initial;
  cursor: pointer;
  display: inline;
  margin: 0px;
  overflow: inherit;
  padding: 0px;
  text-align: left;
  text-overflow: inherit;
  border-bottom: 1px solid transparent;
  user-select: text;
}
</style>
