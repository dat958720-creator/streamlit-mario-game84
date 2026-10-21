
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Multi-Level", layout="centered")

st.title("🍄 Super Mario - Chọn Nhân Vật & Vượt Ải")

# 1. PHẦN CHỌN NHÂN VẬT (Dựa trên 6 mẫu nhân vật)
st.subheader("1. Chọn nhân vật chiến đấu")
col1, col2, col3 = st.columns(3)

# Danh sách nhân vật tương ứng với 6 mẫu trong ảnh
character_dict = {
    "Luigi (Xanh Lá)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Đỏ Truyền Thống)": "https://i.imgur.com/39A4D3B.png",
    "Fire Mario (Trắng/Đỏ)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Đỏ Đậm)": "https://i.imgur.com/39A4D3B.png",
    "Mario (Áo Xanh Dương)": "https://i.imgur.com/39A4D3B.png",
    "Nhân vật Đặc Biệt (Vàng/Đỏ)": "https://i.imgur.com/39A4D3B.png"
}

selected_char_name = st.selectbox("Lựa chọn chiến binh của bạn:", list(character_dict.keys()))
char_image_url = character_dict[selected_char_name]

# 2. PHẦN CHỌN MÀN CHƠI & ĐỘ KHÓ
st.subheader("2. Chọn màn chơi")
level_choice = st.radio(
    "Chọn độ khó:",
    ["Màn 1: Dễ (Nhảy cơ bản, ít vật cản)", "Màn 2: Trung Bình (Tốc độ cao, khoảng cách xa)", "Màn 3: Khó (Trọng lực nặng, thử thách cực đại)"],
    horizontal=True
)

# Xác định thông số theo màn chơi
if "Màn 1" in level_choice:
    level_id = 1
    gravity = 0.8
    jump_power = -12
    obstacle_speed = 0
elif "Màn 2" in level_choice:
    level_id = 2
    gravity = 0.9
    jump_power = -13
    obstacle_speed = 2 # Vật cản di chuyển
else:
    level_id = 3
    gravity = 1.1
    jump_power = -14
    obstacle_speed = 4

st.markdown("---")
st.write(f"🎮 **Đang chơi:** `{selected_char_name}` ở **Màn {level_id}** | Dùng phím **Trái/Phải** để di chuyển, **Lên / Space** để nhảy!")

# 3. MÃ HTML/JS NHÂN VẬT & MÀN CHƠI
mario_game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background-color: #5c94fc; text-align: center; font-family: sans-serif; }}
        canvas {{ background: #5c94fc; border: 4px solid #000; margin-top: 10px; cursor: pointer; }}
        #score-board {{ color: white; font-size: 18px; font-weight: bold; margin-bottom: 5px; }}
    </style>
</head>
<body>
    <div id="score-board">Màn: {level_id} | Nhân vật: {selected_char_name}</div>
    <canvas id="gameCanvas" width="600" height="300"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Âm thanh
        const bgMusic = new Audio("https://www.soundrelish.com/wp-content/uploads/2021/04/Super-Mario-Bros.-Theme-Song.mp3");
        bgMusic.loop = true;
        bgMusic.volume = 0.3;
        const jumpSound = new Audio("https://themushroomkingdom.net/sounds/wav/smb/smb_jump-small.wav");
        jumpSound.volume = 0.5;

        let musicStarted = false;
        function startAudio() {{
            if (!musicStarted) {{
                bgMusic.play().catch(e => {{}});
                musicStarted = true;
            }}
        }}

        // Hình ảnh nhân vật được chọn từ Streamlit
        const marioImg = new Image();
        marioImg.src = "{char_image_url}";

        let mario = {{
            x: 50, y: 200, width: 32, height: 40,
            dx: 0, dy: 0, 
            gravity: {gravity}, 
            jumpPower: {jump_power}, 
            grounded: false
        }};

        const groundY = 250;
        
        // Cấu hình chướng ngại vật theo màn chơi
        let blocks = [
            {{x: 200, y: 170, width: 40, height: 40, speed: {obstacle_speed}}},
            {{x: 350, y: 130, width: 40, height: 40, speed: -{obstacle_speed}}}
        ];

        let keys = {{}};
        window.addEventListener("keydown", (e) => {{ keys[e.code] = true; startAudio(); }});
        window.addEventListener("keyup", (e) => keys[e.code] = false);
        canvas.addEventListener("click", startAudio);

        function update() {{
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

            // Di chuyển chướng ngại vật ở các màn khó
            blocks.forEach(b => {{
                b.x += b.speed;
                if (b.x < 150 || b.x > 450) b.speed *= -1; // Đổi hướng qua lại
            }});

            // Va chạm mặt đất
            if (mario.y + mario.height >= groundY) {{
                mario.y = groundY - mario.height;
                mario.dy = 0;
                mario.grounded = true;
            }}

            // Va chạm gạch
            blocks.forEach(b => {{
                if (mario.x < b.x + b.width && mario.x + mario.width > b.x &&
                    mario.y + mario.height >= b.y && mario.y < b.y + b.height && mario.dy > 0) {{
                    mario.y = b.y - mario.height;
                    mario.dy = 0;
                    mario.grounded = true;
                }}
            }});

            if (mario.x < 0) mario.x = 0;
            if (mario.x + mario.width > canvas.width) mario.x = canvas.width - mario.width;
        }}

        function draw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ Mặt đất
            ctx.fillStyle = "{'#222' if level_id == 3 else ('#e75914' if level_id == 2 else '#00b800')}";
            ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
            ctx.fillStyle = "#00b800";
            ctx.fillRect(0, groundY, canvas.width, 10);

            // Vẽ Gạch
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

            // Vẽ Nhân vật
            if (marioImg.complete) {{
                ctx.drawImage(marioImg, mario.x, mario.y, mario.width, mario.height);
            }} else {{
                ctx.fillStyle = "red";
                ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
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
