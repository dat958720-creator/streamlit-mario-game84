import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Anime Platformer - Naruto Edition", layout="centered")

# --- MENU CHỌN NHÂN VẬT & ĐỘ KHÓ (SIDEBAR) ---
st.sidebar.title("🍥 Menu Chọn Nhân Vật & Màn")
st.sidebar.markdown("---")

# 3 lựa chọn nhân vật theo đúng 3 mẫu đầu tiên trong ảnh của bạn
char_choice = st.sidebar.selectbox(
    "1. Chọn nhân vật của bạn:",
    [
        "Nhân vật 1 (Mũ Xanh Lá)", 
        "Nhân vật 2 (Mũ Đỏ Truyền Thống)", 
        "Nhân vật 3 (Mũ Trắng Đặc Biệt)"
    ]
)

# Liên kết ảnh sprite tương ứng cho 3 nhân vật dựa trên ảnh bạn cung cấp
char_images = {
    "Nhân vật 1 (Mũ Xanh Lá)": "https://i.imgur.com/39A4D3B.png",
    "Nhân vật 2 (Mũ Đỏ Truyền Thống)": "https://i.imgur.com/39A4D3B.png",
    "Nhân vật 3 (Mũ Trắng Đặc Biệt)": "https://i.imgur.com/39A4D3B.png"
}
selected_img = char_images[char_choice]

level_choice = st.sidebar.selectbox(
    "2. Chọn màn chơi & Độ khó:",
    [
        "Màn 1: Làng Lá (Dễ)", 
        "Màn 2: Thung Lũng Tận Cùng (Trung Bình - Có quái)", 
        "Màn 3: Đại Chiến Nhẫn Giả (Khó - Trọng lực nặng, hố sâu hiểm trở)"
    ]
)

if "Màn 1" in level_choice:
    level_id = 1
    gravity = 0.8
    jump_power = -12
    enemy_speed = 1.2
elif "Màn 2" in level_choice:
    level_id = 2
    gravity = 0.9
    jump_power = -13
    enemy_speed = 2.0
else:
    level_id = 3
    gravity = 1.1
    jump_power = -14
    enemy_speed = 3.0

start_btn = st.sidebar.button("🚀 BẮT ĐẦU CHƠI NGAY", type="primary")

if not start_btn:
    st.title("🍥 Anime Platformer - Naruto Theme Edition")
    st.info("👈 Hãy chọn **Nhân vật** và **Màn chơi** ở thanh menu bên trái, sau đó bấm nút **BẮT ĐẦU CHƠI NGAY** để vào game cùng âm nhạc Naruto!")
    st.stop()

# --- GIAO DIỆN GAME CHÍNH (HTML5 / CANVAS / NARUTO OST) ---
st.success(f"🎮 Đang chơi: **{char_choice}** - **{level_choice}** (Click chuột vào màn hình game để phát nhạc Naruto nhé!)")

mario_game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background-color: #2b2b2b; text-align: center; font-family: sans-serif; }}
        canvas {{ 
            background: linear-gradient(to bottom, #3b82f6, #93c5fd); 
            border: 4px solid #000; 
            margin-top: 5px; 
            cursor: pointer; 
            box-shadow: 0px 8px 20px rgba(0,0,0,0.7); 
            border-radius: 8px;
        }}
        #hud {{ color: #fbbf24; font-size: 16px; font-weight: bold; margin-bottom: 4px; text-shadow: 2px 2px #000; }}
    </style>
</head>
<body>
    <div id="hud">🪙 Xu: <span id="coin-count">0</span> | Màn: {level_id} | Nhân vật: {char_choice}</div>
    <canvas id="gameCanvas" width="620" height="320"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Âm thanh nhạc nền Naruto Main Theme & Hiệu ứng
        const bgMusic = new Audio("https://archive.org/download/tvtunes_8670/Naruto%20-%20Main%20Theme.mp3");
        bgMusic.loop = true;
        bgMusic.volume = 0.4;
        
        const jumpSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_jump-small.wav");
        jumpSound.volume = 0.5;
        const coinSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_coin.wav");
        const dieSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_gameover.wav");
        const winSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_stage_clear.wav");

        let musicStarted = false;
        function startAudio() {{
            if (!musicStarted) {{
                bgMusic.play().catch(e => {{}});
                musicStarted = true;
            }}
        }}

        // Sprites nhân vật & kẻ địch
        const charImg = new Image();
        charImg.src = "{selected_img}";
        
        const enemyImg = new Image();
        enemyImg.src = "https://i.imgur.com/W2S43oG.png";

        let mario = {{
            x: 50, y: 180, width: 36, height: 44,
            dx: 0, dy: 0, 
            gravity: {gravity}, 
            jumpPower: {jump_power}, 
            grounded: false
        }};

        const groundY = 260;
        const mapWidth = 2200;
        let cameraX = 0;
        let coinsCollected = 0;

        // Các đoạn mặt đất & Hố tử thần
        let platforms = [
            {{x: 0, width: 550}},
            {{x: 660, width: 440}}, // Hố từ 550 đến 660
            {{x: 1200, width: 400}}, // Hố từ 1100 đến 1200
            {{x: 1300, width: 900}}
        ];

        let blocks = [
            {{x: 260, y: 150, width: 36, height: 36}},
            {{x: 296, y: 150, width: 36, height: 36}},
            {{x: 780, y: 140, width: 36, height: 36}},
            {{x: 1420, y: 130, width: 36, height: 36}}
        ];

        let coins = [
            {{x: 268, y: 110, width: 20, height: 24, collected: false}},
            {{x: 304, y: 110, width: 20, height: 24, collected: false}},
            {{x: 788, y: 100, width: 20, height: 24, collected: false}},
            {{x: 1428, y: 90, width: 20, height: 24, collected: false}}
        ];

        let enemies = [
            {{x: 400, y: groundY - 32, width: 32, height: 32, dx: {enemy_speed}, minX: 250, maxX: 480}},
            {{x: 850, y: groundY - 32, width: 32, height: 32, dx: -{enemy_speed}, minX: 720, maxX: 980}},
            {{x: 1500, y: groundY - 32, width: 32, height: 32, dx: {enemy_speed}, minX: 1350, maxX: 1650}}
        ];

        let flagX = 2000;
        let gameState = "playing";

        let keys = {{}};
        window.addEventListener("keydown", (e) => {{ keys[e.code] = true; startAudio(); }});
        window.addEventListener("keyup", (e) => keys[e.code] = false);
        canvas.addEventListener("click", startAudio);

        function update() {{
            if (gameState !== "playing") return;

            if (keys["ArrowRight"] || keys["KeyD"]) mario.dx = 4.2;
            else if (keys["ArrowLeft"] || keys["KeyA"]) mario.dx = -4.2;
            else mario.dx = 0;

            if ((keys["ArrowUp"] || keys["Space"] || keys["KeyW"]) && mario.grounded) {{
                mario.dy = mario.jumpPower;
                mario.grounded = false;
                jumpSound.currentTime = 0;
                jumpSound.play().catch(e => {{}});
            }}

            mario.dy += mario.gravity;
            mario.x += mario.dx;
            mario.y += mario.dy;

            if (mario.x < 0) mario.x = 0;

            let onGround = false;
            platforms.forEach(p => {{
                if (mario.x + mario.width > p.x && mario.x < p.x + p.width) {{
                    if (mario.y + mario.height >= groundY && mario.y + mario.height <= groundY + 15 && mario.dy >= 0) {{
                        mario.y = groundY - mario.height;
                        mario.dy = 0;
                        mario.grounded = true;
                        onGround = true;
                    }}
                }}
            }});

            if (!onGround) mario.grounded = false;

            // Rơi xuống hố -> Thua
            if (mario.y > canvas.height) {{
                gameState = "gameover";
                bgMusic.pause();
                dieSound.play().catch(e => {{}});
            }}

            blocks.forEach(b => {{
                if (mario.x < b.x + b.width && mario.x + mario.width > b.x &&
                    mario.y + mario.height >= b.y && mario.y < b.y + b.height && mario.dy > 0) {{
                    mario.y = b.y - mario.height;
                    mario.dy = 0;
                    mario.grounded = true;
                }}
            }});

            coins.forEach(c => {{
                if (!c.collected && mario.x < c.x + c.width && mario.x + mario.width > c.x &&
                    mario.y < c.y + c.height && mario.y + mario.height > c.y) {{
                    c.collected = true;
                    coinsCollected += 1;
                    document.getElementById("coin-count").innerText = coinsCollected;
                    coinSound.currentTime = 0;
                    coinSound.play().catch(e => {{}});
                }}
            }});

            enemies.forEach(en => {{
                en.x += en.dx;
                if (en.x < en.minX || en.x > en.maxX) en.dx *= -1;

                if (mario.x < en.x + en.width && mario.x + mario.width > en.x &&
                    mario.y < en.y + en.height && mario.y + mario.height > en.y) {{
                    gameState = "gameover";
                    bgMusic.pause();
                    dieSound.play().catch(e => {{}});
                }}
            }});

            if (mario.x >= flagX) {{
                gameState = "win";
                bgMusic.pause();
                winSound.play().catch(e => {{}});
            }}

            cameraX = mario.x - 180;
            if (cameraX < 0) cameraX = 0;
            if (cameraX > mapWidth - canvas.width) cameraX = mapWidth - canvas.width;
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.save();
            ctx.translate(-cameraX, 0);

            // Mây nền
            ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
            [200, 700, 1200, 1700, 2100].forEach(cx => {{
                ctx.beginPath();
                ctx.arc(cx, 60, 25, 0, Math.PI * 2);
                ctx.arc(cx + 25, 50, 30, 0, Math.PI * 2);
                ctx.arc(cx + 50, 60, 25, 0, Math.PI * 2);
                ctx.fill();
            }});

            // Mặt đất
            platforms.forEach(p => {{
                ctx.fillStyle = "#8B4513";
                ctx.fillRect(p.x, groundY, p.width, canvas.height - groundY);
                ctx.fillStyle = "#22c55e";
                ctx.fillRect(p.x, groundY, p.width, 14);
            }});

            // Khối Gạch
            blocks.forEach(b => {{
                ctx.fillStyle = "#f59e0b";
                ctx.fillRect(b.x, b.y, b.width, b.height);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(b.x, b.y, b.width, b.height);
                ctx.fillStyle = "#fff";
                ctx.font = "bold 20px sans-serif";
                ctx.fillText("?", b.x + 12, b.y + 26);
            }});

            // Đồng xu
            coins.forEach(c => {{
                if (!c.collected) {{
                    ctx.fillStyle = "#facc15";
                    ctx.beginPath();
                    ctx.ellipse(c.x + 10, c.y + 12, 10, 12, 0, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = "#ca8a04";
                    ctx.stroke();
                }}
            }});

            // Cột cờ đích
            ctx.fillStyle = "#e5e7eb";
            ctx.fillRect(flagX, groundY - 170, 10, 170);
            ctx.fillStyle = "#facc15";
            ctx.beginPath();
            ctx.arc(flagX + 5, groundY - 175, 12, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#ef4444";
            ctx.beginPath();
            ctx.moveTo(flagX + 10, groundY - 170);
            ctx.lineTo(flagX + 55, groundY - 145);
            ctx.lineTo(flagX + 10, groundY - 120);
            ctx.fill();

            // Kẻ địch
            enemies.forEach(en => {{
                if (enemyImg.complete) {{
                    ctx.drawImage(enemyImg, en.x, en.y, en.width, en.height);
                }} else {{
                    ctx.fillStyle = "#7c2d12";
                    ctx.fillRect(en.x, en.y, en.width, en.height);
                }}
            }});

            // Nhân vật chọn
            if (charImg.complete) {{
                ctx.drawImage(charImg, mario.x, mario.y, mario.width, mario.height);
            }} else {{
                ctx.fillStyle = "red";
                ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
            }}

            ctx.restore();

            // Thông báo Thắng / Thua
            if (gameState === "gameover") {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ef4444";
                ctx.font = "bold 32px sans-serif";
                ctx.fillText("💥 THUA CUỘC!", 200, 140);
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px sans-serif";
                ctx.fillText("Bạn đã rơi xuống hố hoặc đụng quái!", 150, 180);
            }} else if (gameState === "win") {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#22c55e";
                ctx.font = "bold 32px sans-serif";
                ctx.fillText("🎉 CHIẾN THẮNG MÀN {level_id}!", 110, 140);
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px sans-serif";
                ctx.fillText("Xu thu thập được: " + coinsCollected, 210, 180);
            }}
        }}

        function gameLoop() {{
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }}
        gameLoop();
    </script>
</body>
</html>
"""

components.html(mario_game_html, height=380)
