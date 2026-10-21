
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Bros HD", layout="centered")

# --- MENU CHỌN NHÂN VẬT & ĐỘ KHÓ (SIDEBAR) ---
st.sidebar.title("🍄 Menu Super Mario HD")
st.sidebar.markdown("---")

char_choice = st.sidebar.selectbox(
    "1. Chọn nhân vật chiến đấu:",
    [
        "Mario (Đỏ Truyền Thống)", 
        "Luigi (Xanh Lá)", 
        "Fire Mario (Trắng Đỏ)", 
        "Mario (Áo Đỏ Đậm)", 
        "Mario (Áo Xanh Dương)", 
        "Nhân Vật Đặc Biệt"
    ]
)

# Sprite nhân vật chuẩn HD
char_images = {
    "Mario (Đỏ Truyền Thống)": "https://i.imgur.com/39A4D3B.png",
    "Luigi (Xanh Lá)": "https://i.imgur.com/39A4D3B.png",
    "Fire Mario (Trắng Đỏ)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Đỏ Đậm)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Xanh Dương)": "https://i.imgur.com/39A4D3B.png",
    "Nhân Vật Đặc Biệt": "https://i.imgur.com/39A4D3B.png"
}
selected_img = char_images[char_choice]

level_choice = st.sidebar.selectbox(
    "2. Chọn màn chơi & Độ khó:",
    [
        "Màn 1: Vương Quốc Nấm (Dễ)", 
        "Màn 2: Thung Lũng Cống Xanh (Trung Bình - Có quái Koopa & Goomba)", 
        "Màn 3: Đêm Tối Tử Thần (Khó - Trọng lực nặng, nhiều hố sâu)"
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
    st.title("🌟 Super Mario Bros - HD Graphics Edition")
    st.image("https://i.imgur.com/39A4D3B.png", width=120)
    st.info("👈 Bấm chọn **Nhân vật** và **Màn chơi** ở thanh bên trái, sau đó bấm **BẮT ĐẦU CHƠI NGAY** để trải nghiệm đồ họa HD mượt mà!")
    st.stop()

# --- GIAO DIỆN GAME CHÍNH (CANVAS HTML5 HD) ---
st.success(f"🎮 Đang chơi: **{char_choice}** - **{level_choice}** (Chạy qua hố, ăn xu vàng và nhảy chạm cột cờ 🚩 để thắng!)")

mario_game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background-color: #5c94fc; text-align: center; font-family: sans-serif; }}
        canvas {{ 
            background: linear-gradient(to bottom, #4a90e2, #7eb6ff); 
            border: 4px solid #111; 
            margin-top: 5px; 
            cursor: pointer; 
            box-shadow: 0px 8px 20px rgba(0,0,0,0.6); 
            border-radius: 8px;
        }}
        #hud {{ color: #ffe600; font-size: 16px; font-weight: bold; margin-bottom: 4px; text-shadow: 2px 2px #000; }}
    </style>
</head>
<body>
    <div id="hud">🪙 Xu: <span id="coin-count">0</span> | Màn: {level_id} | Nhân vật: {char_choice}</div>
    <canvas id="gameCanvas" width="620" height="320"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Âm thanh
        const bgMusic = new Audio("https://www.soundrelish.com/wp-content/uploads/2021/04/Super-Mario-Bros.-Theme-Song.mp3");
        bgMusic.loop = true;
        bgMusic.volume = 0.3;
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

        // Sprites Đồ Họa HD
        const marioImg = new Image();
        marioImg.src = "{selected_img}";
        
        const goombaImg = new Image();
        goombaImg.src = "https://i.imgur.com/W2S43oG.png"; // Quái Goomba HD

        let mario = {{
            x: 50, y: 180, width: 34, height: 44,
            dx: 0, dy: 0, 
            gravity: {gravity}, 
            jumpPower: {jump_power}, 
            grounded: false
        }};

        const groundY = 260;
        const mapWidth = 2200;
        let cameraX = 0;
        let coinsCollected = 0;

        // Mặt đất & Hố sâu
        let platforms = [
            {{x: 0, width: 550}},
            {{x: 650, width: 450}}, // Hố từ 550 đến 650
            {{x: 1180, width: 400}}, // Hố từ 1100 đến 1180
            {{x: 1280, width: 920}}
        ];

        // Khối Gạch & Cống Xanh (Pipes)
        let blocks = [
            {{x: 250, y: 160, width: 36, height: 36}},
            {{x: 286, y: 160, width: 36, height: 36}},
            {{x: 322, y: 160, width: 36, height: 36}},
            {{x: 750, y: 150, width: 36, height: 36}},
            {{x: 820, y: 150, width: 36, height: 36}},
            {{x: 1400, y: 140, width: 36, height: 36}}
        ];

        let pipes = [
            {{x: 450, y: groundY - 50, width: 45, height: 50}},
            {{x: 950, y: groundY - 65, width: 45, height: 65}},
            {{x: 1600, y: groundY - 50, width: 45, height: 50}}
        ];

        // Đồng xu vàng HD (Coins)
        let coins = [
            {{x: 258, y: 120, width: 20, height: 24, collected: false}},
            {{x: 294, y: 120, width: 20, height: 24, collected: false}},
            {{x: 758, y: 110, width: 20, height: 24, collected: false}},
            {{x: 1000, y: groundY - 40, width: 20, height: 24, collected: false}},
            {{x: 1408, y: 100, width: 20, height: 24, collected: false}}
        ];

        // Kẻ Địch Goomba HD
        let enemies = [
            {{x: 380, y: groundY - 32, width: 32, height: 32, dx: {enemy_speed}, minX: 250, maxX: 440}},
            {{x: 850, y: groundY - 32, width: 32, height: 32, dx: -{enemy_speed}, minX: 700, maxX: 940}},
            {{x: 1450, y: groundY - 32, width: 32, height: 32, dx: {enemy_speed}, minX: 1350, maxX: 1580}}
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

            // Xử lý đứng trên mặt đất
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

            // Va chạm Hố tử thần
            if (mario.y > canvas.height) {{
                gameState = "gameover";
                bgMusic.pause();
                dieSound.play().catch(e => {{}});
            }}

            // Va chạm Gạch
            blocks.forEach(b => {{
                if (mario.x < b.x + b.width && mario.x + mario.width > b.x &&
                    mario.y + mario.height >= b.y && mario.y < b.y + b.height && mario.dy > 0) {{
                    mario.y = b.y - mario.height;
                    mario.dy = 0;
                    mario.grounded = true;
                }}
            }});

            // Va chạm Cống Xanh
            pipes.forEach(p => {{
                if (mario.x < p.x + p.width && mario.x + mario.width > p.x &&
                    mario.y + mario.height >= p.y && mario.y < p.y + p.height) {{
                    if (mario.dy > 0 && mario.y + mario.height - mario.dy <= p.y) {{
                        mario.y = p.y - mario.height;
                        mario.dy = 0;
                        mario.grounded = true;
                    }} else {{
                        if (mario.dx > 0) mario.x = p.x - mario.width;
                        else if (mario.dx < 0) mario.x = p.x + p.width;
                    }}
                }}
            }});

            // Ăn Đồng Xu Vàng (Coins)
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

            // Di chuyển Quái & Va chạm
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

            // Chạm Vạch Cột Cờ Đích
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

            // 1. Mây Trôi Bầu Trời HD
            ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
            [200, 600, 1100, 1600, 2000].forEach(cx => {{
                ctx.beginPath();
                ctx.arc(cx, 60, 25, 0, Math.PI * 2);
                ctx.arc(cx + 25, 50, 30, 0, Math.PI * 2);
                ctx.arc(cx + 50, 60, 25, 0, Math.PI * 2);
                ctx.fill();
            }});

            // 2. Mặt Đất HD (Màu Cỏ Chuẩn Super Mario)
            platforms.forEach(p => {{
                // Đất nâu hạt
                ctx.fillStyle = "#c84c0c";
                ctx.fillRect(p.x, groundY, p.width, canvas.height - groundY);
                // Cỏ xanh ngọc HD
                ctx.fillStyle = "#00a800";
                ctx.fillRect(p.x, groundY, p.width, 14);
                ctx.fillStyle = "#fc2800"; // Họa tiết hoa viên gạch nhỏ
                for(let gx = p.x; gx < p.x + p.width; gx += 30) {{
                    ctx.fillRect(gx, groundY + 20, 6, 6);
                }}
            }});

            // 3. Cống Xanh (Green Pipes HD)
            pipes.forEach(p => {{
                ctx.fillStyle = "#00a800";
                ctx.fillRect(p.x, p.y, p.width, p.height);
                ctx.fillStyle = "#00e800"; // Vệt sáng mượt
                ctx.fillRect(p.x + 4, p.y, 8, p.height);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(p.x, p.y, p.width, p.height);
                // Đầu cống
                ctx.fillStyle = "#00a800";
                ctx.fillRect(p.x - 4, p.y, p.width + 8, 16);
                ctx.strokeRect(p.x - 4, p.y, p.width + 8, 16);
            }});

            // 4. Khối Gạch Hỏi Chấm HD
            blocks.forEach(b => {{
                ctx.fillStyle = "#fba100";
                ctx.fillRect(b.x, b.y, b.width, b.height);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(b.x, b.y, b.width, b.height);
                ctx.fillStyle = "#fff";
                ctx.font = "bold 20px sans-serif";
                ctx.fillText("?", b.x + 12, b.y + 26);
            }});

            // 5. Đồng Xu Vàng (Coins HD)
            coins.forEach(c => {{
                if (!c.collected) {{
                    ctx.fillStyle = "#ffd700";
                    ctx.beginPath();
                    ctx.ellipse(c.x + 10, c.y + 12, 10, 12, 0, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = "#d4af37";
                    ctx.stroke();
                }}
            }});

            // 6. Cột Cờ Đích HD (Finish Flag)
            ctx.fillStyle = "#e0e0e0";
            ctx.fillRect(flagX, groundY - 170, 10, 170);
            ctx.fillStyle = "#ffd700"; // Quả cầu vàng trên đỉnh
            ctx.beginPath();
            ctx.arc(flagX + 5, groundY - 175, 12, 0, Math.PI * 2);
            ctx.fill();

            ctx.fillStyle = "#fc2800"; // Cờ đỏ
            ctx.beginPath();
            ctx.moveTo(flagX + 10, groundY - 170);
            ctx.lineTo(flagX + 55, groundY - 145);
            ctx.lineTo(flagX + 10, groundY - 120);
            ctx.fill();

            // 7. Kẻ Địch Goomba HD
            enemies.forEach(en => {{
                if (goombaImg.complete) {{
                    ctx.drawImage(goombaImg, en.x, en.y, en.width, en.height);
                }} else {{
                    ctx.fillStyle = "#a04000";
                    ctx.fillRect(en.x, en.y, en.width, en.height);
                }}
            }});

            // 8. Nhân Vật Mario HD
            if (marioImg.complete) {{
                ctx.drawImage(marioImg, mario.x, mario.y, mario.width, mario.height);
            }} else {{
                ctx.fillStyle = "red";
                ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
            }}

            ctx.restore();

            // Thắng / Thua Screen Overlay
            if (gameState === "gameover") {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ff3333";
                ctx.font = "bold 32px sans-serif";
                ctx.fillText("💥 GAME OVER!", 200, 140);
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px sans-serif";
                ctx.fillText("Rơi hố hoặc đụng quái! Tải lại trang để chơi lại.", 110, 180);
            }} else if (gameState === "win") {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.85)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#00ff00";
                ctx.font = "bold 32px sans-serif";
                ctx.fillText("🎉 CHIẾN THẮNG MÀN {level_id}!", 110, 140);
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px sans-serif";
                ctx.fillText("Tuyệt vời! Bạn thu thập được " + coinsCollected + " xu vàng!", 110, 180);
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
