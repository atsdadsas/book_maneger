
// --- 1. スライドショー機能 ---
const images = [
    "/static/images/run/1.jpg",
    "/static/images/run/2.jpg",
    "/static/images/run/3.jpg",
    "/static/images/run/4.jpg",
    "/static/images/run/5.jpg",
    "/static/images/run/6.jpg",
    "/static/images/run/7.jpg",
    "/static/images/run/6.jpg",
    "/static/images/run/5.jpg",
    "/static/images/run/4.jpg",
    "/static/images/run/3.jpg",
    "/static/images/run/2.jpg"
];
let currentIndex = 0;

setInterval(() => {
    const imgElement = document.getElementById("target-image");
    if (imgElement) {
        currentIndex = (currentIndex + 1) % images.length;
        imgElement.src = images[currentIndex];
    }
}, 100);

// --- 2. 時計機能 ---
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleString('ja-JP', { 
        year:'numeric', month:'2-digit', day:'2-digit', 
        weekday:'short', hour:'2-digit', minute:'2-digit', second:'2-digit' 
    });
    const clockElement = document.getElementById('realtime-clock');
    if (clockElement) {
        clockElement.textContent = "現在時刻: " + timeString;
    }
}
setInterval(updateClock, 1000);
updateClock();

// --- 3. スタート画面アニメーション ---
window.onload = function() {
    const container = document.getElementById('circle-container');
    const overlay = document.getElementById('opening-overlay');
    
    // 繰り返したい文字リスト
    const message = ["１", "１", "０", "０", "１"]; 

    if (container) {
        // 5x5の二重ループで丸と文字を生成
        for (let i = 0; i < 5; i++) {
            for (let j = 0; j < 5; j++) {
                const circle = document.createElement('div');
                circle.classList.add('white-circle');
                
                // 丸の中に文字を入れる（S,T,A,R,Tを繰り返す）
                circle.textContent = message[j]; 
                
                // 出現タイミングを少しずつずらす演出
                circle.style.animationDelay = ((i * 5 + j) * 0.05) + "s";

                container.appendChild(circle);
            }
        }
    }

    // 5秒後にオーバーレイを解除
    setTimeout(() => {
        if (overlay) {
            overlay.style.opacity = '0'; // フェードアウト
            document.body.classList.remove('no-scroll'); // スクロール解禁
            
            // 完全に消えたら要素を削除
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 1000);
        }
    }, 2000);
};