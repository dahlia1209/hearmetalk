export function getFormattedDate(): string {
    // 現在の日時を取得
    const now = new Date();

    // 日時を 'yyyyMMdd_hhmmss' 形式に整形
    const yyyy = now.getFullYear();
    const MM = String(now.getMonth() + 1).padStart(2, '0'); // 月は0から始まるため+1する
    const dd = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    return `${yyyy}${MM}${dd}_${hh}${mm}${ss}`;
}