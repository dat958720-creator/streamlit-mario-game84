import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Ultimate Edition", layout="centered")

# --- MÀN HÌNH CHÍNH / MENU CHỌN (HOME) ---
st.title("🍄 Super Mario: Cuộc Phiêu Lưu Kì Thú")
st.markdown("---")

st.sidebar.header("⚙️ Cài đặt Trò Chơi")

# 1. Chọn nhân vật (6 nhân vật chuẩn theo hình ảnh của bạn)
char_choice = st.sidebar.selectbox(
    "Chọn nhân vật của bạn:",
    [
        "Luigi (Xanh Lá)", 
        "Mario (Đỏ Truyền Thống)", 
        "Fire Mario (Trắng Đỏ)", 
        "Mario (Áo Đỏ Đậm)", 
        "Mario (Áo Xanh Dương)", 
        "Nhân Vật Đặc Biệt"
    ]
)

# Link ảnh sprite tương ứng cho 6 nhân vật
char_images = {
    "Luigi (Xanh Lá)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Đỏ Truyền Thống)": "https://i.imgur.com/39A4D3B.png",
    "Fire Mario (Trắng Đỏ)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Đỏ Đậm)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Xanh Dương)": "https://i.imgur.com/39A4D3B.png",
    "Nhân Vật Đặc Biệt": "https://i.imgur.com/39A4D3B.png"
}
selected_img = char_images[char_choice]

# 2. Chọn màn chơi & độ khó
level_choice = st.sidebar.selectbox(
    "Chọn màn chơi:",
    [
        "Màn 1: Khởi Động (Dễ)", 
        "Màn 2: Thử Thách (Trung Bình - Vật cản di chuyển)", 
        "Màn 3: Quyết Sát (Khó - Trọng lực nặng & Tốc độ cao)"
    ]
)

if "Màn 1" in level_choice:
    level_id = 1
    gravity = 0.8
    jump_power = -12
    obstacle_speed = 0
elif "Màn 2" in level_choice:
    level_id = 2
    gravity = 0.9
    jump_power = -13
    obstacle_speed = 2
else:
    level_id = 3
    gravity = 1.1
    jump_power = -14
    obstacle_speed = 4

# Nút bắt đầu chơi
start_game = st.sidebar.button("🚀 BẮT ĐẦU CHƠI NGAY", type="primary")

if not start_game:
    st.info("👈 Hãy chọn **Nhân vật** và **Màn chơi** ở thanh bên trái (Sidebar), sau đó bấm nút **BẮT ĐẦU CHƠI NGAY** để vào game!")
    st.stop()

# --- GIAO DIỆN GAME CHÍNH (HTML5 / CANVAS / JS) ---
st.success(f"🎮 Đang chơi: **{char_choice}** tại **{level_choice}**! (Click chuột vào khung game để bật nhạc)")

mario_game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background-color: #5c94fc; text-align: center; font-family: sans-serif; }}
        canvas {{ background: #5c94fc; border: 4px solid #000; margin-top: 5px; cursor: pointer; box-shadow: 0px 4px 10px rgba(0,0,0,0.5); }}
        #ui-bar {{ color: white; font-size: 16px; font-weight: bold; margin-bottom: 3px; text-shadow: 2px 2px #000; }}
    </style>
</head>
<body>
    <div id="ui-bar">Màn: {level_id} | Nhân vật: {char_choice} | Mục tiêu: Chạy đến Cột Cờ Đích 🚩 bên phải!</div>
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

        let mario = {{
            x: 50, y: 200, width: 32, height: 40,
            dx: 0, dy: 0, 
            gravity: {gravity}, 
            jumpPower: {jump_power}, 
            grounded: false
        }};

        const groundY = 250;
        
        // Khối gạch và Vạch đích
        let blocks = [
            {{x: 180, y: 170, width: 40, height: 40, speed: {obstacle_speed}}},
            {{x: 340, y: 130, width: 40, height: 40, speed: -{obstacle_speed}}}
        ];

        let flagPole = {{ x: 520, y: 100, width: 15, height: 150 }};
        let gameWon = false;

        let keys = {{}};
        window.addEventListener("keydown", (e) => {{ keys[e.code] = true; startAudio(); }});
        window.addEventListener("keyup", (e) => keys[e.code] = false);
        canvas.addEventListener("click", startAudio);

        function update() {{
            if (gameWon) return;

            if (keys["ArrowRight"] || keys["KeyD"]) mario.dx = 4;
            else if (keys["ArrowLeft"] || keys["KeyA"]) mario.dx = -4;
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

            // Vật cản di chuyển (Màn 2 & 3)
            blocks.forEach(b => {{
                b.x += b.speed;
                if (b.x < 150 || b.x > 450) b.speed *= -1;
            }});

            // Va chạm mặt đất
            if (mario.y + mario.height >= groundY) {{
                mario.y = groundY - mario.height;
                mario.dy = 0;
                mario.grounded = true;
            }}

            // Va chạm gạch hỏi chấm
            blocks.forEach(b => {{
                if (mario.x < b.x + b.width && mario.x + mario.width > b.x &&
                    mario.y + mario.height >= b.y && mario.y < b.y + b.height && mario.dy > 0) {{
                    mario.y = b.y - mario.height;
                    mario.dy = 0;
                    mario.grounded = true;
                }}
            }});

            // Kiểm tra chiến thắng (Chạm vạch đích cột cờ)
            if (mario.x + mario.width >= flagPole.x && mario.y + mario.height >= groundY - flagPole.height) {{
                gameWon = true;
                bgMusic.pause();
                winSound.play().catch(e => {{}});
            }}

            if (mario.x < 0) mario.x = 0;
            if (mario.x + mario.width > canvas.width) mario.x = canvas.width - mario.width;
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ Bầu trời & Mặt đất
            ctx.fillStyle = level_id == 3 ? "#2b2b2b" : "#5c94fc";
            ctx.fillRect(0, 0, canvas.width, groundY);
            
            ctx.fillStyle = "#e75914"; // Đất nền
            ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
            ctx.fillStyle = "#00b800"; // Cỏ
            ctx.fillRect(0, groundY, canvas.width, 10);

            // 2. Vẽ Cột cờ Vạch Đích (Finish Flag)
            ctx.fillStyle = "#fff";
            ctx.fillRect(flagPole.x, groundY - flagPole.height, flagPole.width, flagPole.height);
            // Lá cờ chiến thắng
            ctx.fillStyle = "#ff0000";
            ctx.beginPath();
            ctx.moveTo(flagPole.x + flagPole.width, groundY - flagPole.height);
            ctx.lineTo(flagPole.x + flagPole.width + 40, groundY - flagPole.height + 20);
            ctx.lineTo(flagPole.x + flagPole.width, groundY - flagPole.height + 40);
            ctx.fill();

            // 3. Vẽ Khối Gạch
            blocks.forEach(b => {{
                ctx.fillStyle = level_id == 3 ? "#ff3333" : "#fba100";
                ctx.fillRect(b.x, b.y, b.width, b.height);
                ctx.strokeStyle = "#000";
                ctx.lineWidth = 2;
                ctx.strokeRect(b.x, b.y, b.width, b.height);
                
                ctx.fillStyle = "#fff";
                ctx.font = "bold 20px sans-serif";
                ctx.fillText("?", b.x + 14, b.y + 27);
            }});

            // 4. Vẽ Nhân vật
            if (marioImg.complete) {{
                ctx.drawImage(marioImg, mario.x, mario.y, mario.width, mario.height);
            }} else {{
                ctx.fillStyle = "red";
                ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
            }}

            // 5. Hiển thị thông báo chiến thắng khi về đích
            if (gameWon) {{
                ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = "#00ff00";
                ctx.font = "bold 32px sans-serif";
                ctx.fillText("🎉 CHIẾN THẮNG MÀN {level_id}!", 100, 130);
                ctx.fillStyle = "#ffffff";
                ctx.font = "18px sans-serif";
                ctx.fillText("Tuyệt vời! Hãy load lại trang để chơi màn tiếp theo.", 110, 170);
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

