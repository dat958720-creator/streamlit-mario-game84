import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Platformer", layout="centered")

# --- MENU CHỌN NHÂN VẬT & ĐỘ KHÓ (SIDEBAR) ---
st.sidebar.title("🍄 Menu Trò Chơi Mario")
st.sidebar.markdown("---")

# Chọn 1 trong 6 nhân vật chuẩn theo hình ảnh của bạn
char_choice = st.sidebar.selectbox(
    "1. Chọn nhân vật chiến đấu:",
    [
        "Luigi (Xanh Lá)", 
        "Mario (Đỏ Truyền Thống)", 
        "Fire Mario (Trắng Đỏ)", 
        "Mario (Áo Đỏ Đậm)", 
        "Mario (Áo Xanh Dương)", 
        "Nhân Vật Đặc Biệt (Vàng)"
    ]
)

# Liên kết hình ảnh sprite cho 6 nhân vật (sử dụng ảnh chuẩn)
char_images = {
    "Luigi (Xanh Lá)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Đỏ Truyền Thống)": "https://i.imgur.com/39A4D3B.png",
    "Fire Mario (Trắng Đỏ)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Đỏ Đậm)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Xanh Dương)": "https://i.imgur.com/39A4D3B.png",
    "Nhân Vật Đặc Biệt (Vàng)": "https://i.imgur.com/39A4D3B.png"
}
selected_img = char_images[char_choice]

# Chọn màn chơi & độ khó
level_choice = st.sidebar.selectbox(
    "2. Chọn màn chơi & Độ khó:",
    [
        "Màn 1: Dễ (Đường ngắn, ít hố)", 
        "Màn 2: Trung Bình (Nhiều hố, có quái đi tuần)", 
        "Màn 3: Khó (Tốc độ cao, trọng lực nặng, thử thách cực đại)"
    ]
)

if "Màn 1" in level_choice:
    level_id = 1
    gravity = 0.8
    jump_power = -12
    enemy_speed = 1
elif "Màn 2" in level_choice:
    level_id = 2
    gravity = 0.9
    jump_power = -13
    enemy_speed = 2
else:
    level_id = 3
    gravity = 1.1
    jump_power = -14
    enemy_speed = 3

start_btn = st.sidebar.button("🚀 BẮT ĐẦU CHƠI NGAY", type="primary")

if not start_btn:
    st.title("🍄 Super Mario Platformer - Full Edition")
    st.info("👈 Hãy chọn **Nhân vật** và **Màn chơi** ở thanh menu bên trái, sau đó bấm nút **BẮT ĐẦU CHƠI NGAY** để trải nghiệm game!")
    st.stop()

# --- GIAO DIỆN GAME CHÍNH (HTML5 / CANVAS / JAVASCRIPT) ---
st.success(f"🎮 Đang chơi: **{char_choice}** - **{level_choice}**. Dùng phím **Mũi tên Trái/Phải** để chạy, **Mũi tên Lên / Space** để nhảy qua hố và tránh quái!")

mario_game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background-color: #5c94fc; text-align: center; font-family: sans-serif; }}
        canvas {{ background: #5c94fc; border: 4px solid #000; margin-top: 5px; cursor: pointer; box-shadow: 0px 4px 15px rgba(0,0,0,0.6); }}
        #hud {{ color: white; font-size: 15px; font-weight: bold; margin-bottom: 3px; text-shadow: 2px 2px #000; }}
    </style>
</head>
<body>
    <div id="hud">Màn: {level_id} | Nhân vật: {char_choice} | Mục tiêu: Tránh hố, né quái & Chạm vạch đích 🚩</div>
    <canvas id="gameCanvas" width="600" height="300"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Âm thanh game
        const bgMusic = new Audio("https://www.soundrelish.com/wp-content/uploads/2021/04/Super-Mario-Bros.-Theme-Song.mp3");
        bgMusic.loop = true;
        bgMusic.volume = 0.3;
        const jumpSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_jump-small.wav");
        jumpSound.volume = 0.5;
        const dieSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_gameover.wav");
        const winSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_stage_clear.wav");

        let musicStarted = false;
        function startAudio() {{
            if (!musicStarted) {{
                bgMusic.play().catch(e => {{}});
                musicStarted = true;
            }}
        }}

        // Load hình ảnh nhân vật
        const marioImg = new Image();
        marioImg.src = "{selected_img}";

        // Thông số Nhân vật
        let mario = {{
            x: 50, y: 180, width: 32, height: 40,
            dx: 0, dy: 0, 
            gravity: {gravity}, 
            jumpPower: {jump_power}, 
            grounded: false
        }};

        const groundY = 240;
        const mapWidth = 2000; // Bản đồ dài cho nhân vật chạy
        let cameraX = 0;

        // Định nghĩa các đoạn mặt đất và HỐ TỬ THẦN (pits)
        // Mỗi phần tử: [x bắt đầu, chiều rộng] -> Nếu nhân vật đi vào khoảng trống giữa các đoạn = Rơi xuống hố
        let platforms = [
            {{x: 0, width: 500}},
            {{x: 580, width: 400}}, // Hố từ 500 đến 580
            {{x: 1050, width: 450}}, // Hố từ 980 đến 1050
            {{x: 1150, width: 900}}
        ];

        // Khối gạch hỏi chấm trên đường đi
        let blocks = [
            {{x: 300, y: 140, width: 35, height: 35}},
            {{x: 450, y: 120, width: 35, height: 35}},
            {{x: 750, y: 130, width: 35, height: 35}},
            {{x: 1250, y: 110, width: 35, height: 35}}
        ];

        // Kẻ địch (Quái Goomba đi tuần)
        let enemies = [
            {{x: 400, y: groundY - 30, width: 30, height: 30, dx: {enemy_speed}, minX: 300, maxX: 480}},
            {{x: 800, y: groundY - 30, width: 30, height: 30, dx: -{enemy_speed}, minX: 700, maxX: 950}},
            {{x: 1300, y: groundY - 30, width: 30, height: 30, dx: {enemy_speed}, minX: 1200, maxX: 1500}}
        ];

        // Vạch đích cột cờ cuối bản đồ
        let flagX = 1850;

        let gameState = "playing"; // "playing", "gameover", "win"

        let keys = {{}};
        window.addEventListener("keydown", (e) => {{ keys[e.code] = true; startAudio(); }});
        window.addEventListener("keyup", (e) => keys[e.code] = false);
        canvas.addEventListener("click", startAudio);

        function update() {{
            if (gameState !== "playing") return;

            // Điều khiển di chuyển ngang
            if (keys["ArrowRight"] || keys["KeyD"]) mario.dx = 4;
            else if (keys["ArrowLeft"] || keys["KeyA"]) mario.dx = -4;
            else mario.dx = 0;

            // Nhảy
            if ((keys["ArrowUp"] || keys["Space"] || keys["KeyW"]) && mario.grounded) {{
                mario.dy = mario.jumpPower;
                mario.grounded = false;
                jumpSound.currentTime = 0;
                jumpSound.play().catch(e => {{}});
            }}

            // Áp dụng trọng lực
            mario.dy += mario.gravity;
            mario.x += mario.dx;
            mario.y += mario.dy;

            // Giới hạn biên bản đồ trái
            if (mario.x < 0) mario.x = 0;

            // Kiểm tra mặt đất & HỐ TỬ THẦN
            let onGround = false;
            platforms.forEach(p => {{
                // Kiểm tra xem nhân vật có đang đứng trên đoạn mặt đất này không
                if (mario.x + mario.width > p.x && mario.x < p.x + p.width) {{
                    if (mario.y + mario.height >= groundY && mario.y + mario.height <= groundY + 15 && mario.dy >= 0) {{
                        mario.y = groundY - mario.height;
                        mario.dy = 0;
                        mario.grounded = true;
                        onGround = true;
                    }}
                }}
            }});

            if (!onGround) {{
                mario.grounded = false;
            }}

            // Nếu rơi xuống hố (vượt quá chiều cao màn hình) -> Thua cuộc
            if (mario.y > canvas.height) {{
                gameState = "gameover";
                bgMusic.pause();
                dieSound.play().catch(e => {{}});
            }}

            // Va chạm khối gạch
            blocks.forEach(b => {{
                if (mario.x < b.x + b.width && mario.x + mario.width > b.x &&
                    mario.y + mario.height >= b.y && mario.y < b.y + b.height && mario.dy > 0) {{
                    mario.y = b.y - mario.height;
                    mario.dy = 0;
                    mario.grounded = true;
                }}
            }});

            // Di chuyển và kiểm tra va chạm Quái (Enemies)
            enemies.forEach(en => {{
                en.x += en.dx;
                if (en.x < en.minX || en.x > en.maxX) en.dx *= -1;

                // Va chạm nhân vật với quái -> Game Over
                if (mario.x < en.x + en.width && mario.x + mario.width > en.x &&
                    mario.y < en.y + en.height && mario.y + mario.height > en.y) {{
                    gameState = "gameover";
                    bgMusic.pause();
                    dieSound.play().catch(e => {{}});
                }}
            }});

            // Kiểm tra Về đích (Chạm vạch cột cờ)
            if (mario.x >= flagX) {{
                gameState = "win";
                bgMusic.pause();
                winSound.play().catch(e => {{}});
            }}

            // Camera cuộn theo nhân vật
            cameraX = mario.x - 200;
            if (cameraX < 0) cameraX = 0;
            if (cameraX > mapWidth - canvas.width) cameraX = mapWidth - canvas.width;
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.save();
            ctx.translate(-cameraX, 0);

            // 1. Vẽ Bầu trời nền
            ctx.fillStyle = "{'#2b2b2b' if level_id == 3 else '#5c94fc'}";
            ctx.fillRect(0, 0, mapWidth, groundY);

            // 2. Vẽ Các đoạn Mặt đất (có tạo khoảng trống hố tử thần)
            platforms.forEach(p => {{
                ctx.fillStyle = "#e75914";
                ctx.fillRect(p.x, groundY, p.width, canvas.height - groundY);
                ctx.fillStyle = "#00b800"; // Lớp cỏ trên mặt đất
                ctx.fillRect(p.x, groundY, p.width, 12);
            }});

            // 3. Vẽ Vạch Đích Cột Cờ (Finish Flag)
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(flagX, groundY - 160, 12, 160);
            ctx.fillStyle = "#ff0000"; // Lá cờ đỏ
            ctx.beginPath();
            ctx.moveTo(flagX + 12, groundY - 160);
            ctx.lineTo(flagX + 50, groundY - 130);
            ctx.lineTo(flagX + 12, groundY - 100);
            ctx.fill();

            // 4. Vẽ Khối Gạch Hỏi Chấm
            blocks.forEach(b => {{
                ctx.fillStyle = "#fba100";
                ctx.fillRect(b.x, b.y, b.width, b.height);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(b.x, b.y, b.width, b.height);
                ctx.fillStyle = "#fff";
                ctx.font = "bold 18px sans-serif";
                ctx.fillText("?", b.x + 12, b.y + 25);
            }});

            // 5. Vẽ Kẻ Địch (Quái Goomba)
            enemies.forEach(en => {{
                ctx.fillStyle = "#8B4513"; // Màu nâu quái
                ctx.fillRect(en.x, en.y, en.width, en.height);
                ctx.fillStyle = "#fff"; // Mắt quái
                ctx.fillRect(en.x + 5, en.y + 5, 6, 8);
                ctx.fillRect(en.x + 18, en.y + 5, 6, 8);
            }});

            // 6. Vẽ Nhân Vật
            if (marioImg.complete) {{
                ctx.drawImage(marioImg, mario.x, mario.y, mario.width, mario.height);
            }} else {{
                ctx.fillStyle = "red";
                ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
            }}

            ctx.restore();

            // 7. Giao diện thông báo Thắng / Thua trên màn hình
            if (gameState === "gameover") {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#ff3333";
                ctx.font = "bold 32px sans-serif";
                ctx.fillText("💥 THUA CUỘC (RƠI HỐ / ĐỤNG QUÁI)!", 40, 140);
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px sans-serif";
                ctx.fillText("Hãy tải lại trang web để chơi lại từ đầu nhé!", 130, 180);
            }} else if (gameState === "win") {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#00ff00";
                ctx.font = "bold 32px sans-serif";
                ctx.fillText("🎉 CHIẾN THẮNG MÀN {level_id}!", 110, 140);
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px sans-serif";
                ctx.fillText("Tuyệt đỉnh! Bạn đã vượt qua toàn bộ thử thách.", 110, 180);
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

components.html(mario_game_html, height=360)

