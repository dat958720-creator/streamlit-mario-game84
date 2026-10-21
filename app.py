import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Streamlit", layout="centered")

st.title("🍄 Super Mario Mini - Sound & Graphics Edition")
st.write("🎮 Dùng phím **Trái/Phải** để di chuyển, **Lên / Space** để nhảy!")
st.info("🔊 **Mẹo âm thanh:** Nhấp chuột vào khung game một lần để bật Nhạc nền & Âm thanh nhảy!")

# Mã HTML/JS nâng cấp đồ họa & âm thanh
mario_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #5c94fc; text-align: center; font-family: sans-serif; }
        canvas { background: #5c94fc; border: 4px solid #000; margin-top: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="600" height="300"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // 1. CHÈN ÂM THANH
        const bgMusic = new Audio("https://www.soundrelish.com/wp-content/uploads/2021/04/Super-Mario-Bros.-Theme-Song.mp3");
        bgMusic.loop = true;
        bgMusic.volume = 0.3;

        const jumpSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_jump-small.wav");
        jumpSound.volume = 0.5;

        let musicStarted = false;
        function startAudio() {
            if (!musicStarted) {
                bgMusic.play().catch(e => console.log("Audio play blocked until interaction"));
                musicStarted = true;
            }
        }

        // 2. CHÈN HÌNH ẢNH (SPRITES)
        const marioImg = new Image();
        marioImg.src = "https://i.imgur.com/39A4D3B.png"; // Hình ảnh Mario

        // Nhân vật Mario
        let mario = {
            x: 50, y: 200, width: 32, height: 40,
            dx: 0, dy: 0, gravity: 0.8, jumpPower: -12, grounded: false
        };

        const groundY = 250;
        const blocks = [
            {x: 200, y: 170, width: 40, height: 40},
            {x: 240, y: 170, width: 40, height: 40},
            {x: 380, y: 130, width: 40, height: 40}
        ];

        let keys = {};
        window.addEventListener("keydown", (e) => {
            keys[e.code] = true;
            startAudio(); // Tự động phát nhạc khi bấm phím
        });
        window.addEventListener("keyup", (e) => keys[e.code] = false);
        canvas.addEventListener("click", startAudio);

        function update() {
            if (keys["ArrowRight"] || keys["KeyD"]) mario.dx = 4;
            else if (keys["ArrowLeft"] || keys["KeyA"]) mario.dx = -4;
            else mario.dx = 0;

            if ((keys["ArrowUp"] || keys["Space"] || keys["KeyW"]) && mario.grounded) {
                mario.dy = mario.jumpPower;
                mario.grounded = false;
                jumpSound.currentTime = 0;
                jumpSound.play().catch(e => {});
            }

            mario.dy += mario.gravity;
            mario.x += mario.dx;
            mario.y += mario.dy;

            if (mario.y + mario.height >= groundY) {
                mario.y = groundY - mario.height;
                mario.dy = 0;
                mario.grounded = true;
            }

            blocks.forEach(b => {
                if (mario.x < b.x + b.width && mario.x + mario.width > b.x &&
                    mario.y + mario.height >= b.y && mario.y < b.y + b.height && mario.dy > 0) {
                    mario.y = b.y - mario.height;
                    mario.dy = 0;
                    mario.grounded = true;
                }
            });

            if (mario.x < 0) mario.x = 0;
            if (mario.x + mario.width > canvas.width) mario.x = canvas.width - mario.width;
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ Mặt đất
            ctx.fillStyle = "#e75914";
            ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
            ctx.fillStyle = "#00b800";
            ctx.fillRect(0, groundY, canvas.width, 10);

            // Vẽ Các khối gạch Hỏi chấm / Đất
            blocks.forEach(b => {
                ctx.fillStyle = "#fba100";
                ctx.fillRect(b.x, b.y, b.width, b.height);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(b.x, b.y, b.width, b.height);
                
                // Dấu hỏi chấm trên gạch
                ctx.fillStyle = "#fff";
                ctx.font = "bold 20px sans-serif";
                ctx.fillText("?", b.x + 14, b.y + 27);
            });

            // Vẽ Mario bằng Hình ảnh (Sprite)
            if (marioImg.complete) {
                ctx.drawImage(marioImg, mario.x, mario.y, mario.width, mario.height);
            } else {
                ctx.fillStyle = "red";
                ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
            }
        }

        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

components.html(mario_game_html, height=380)
