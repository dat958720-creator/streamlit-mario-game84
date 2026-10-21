import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Streamlit", layout="centered")

st.title("🍄 Super Mario Mini - Streamlit Edition")
st.write("Dùng phím **Mũi tên Trái/Phải** để di chuyển và **Mũi tên Lên (hoặc Space)** để nhảy!")

mario_game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background-color: #5c94fc; text-align: center; font-family: sans-serif; }
        canvas { background: #5c94fc; border: 4px solid #000; margin-top: 10px; }
    </style>
</head>
<body>
    <canvas id="gameCanvas" width="600" height="300"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let mario = {
            x: 50, y: 200, width: 30, height: 40,
            dx: 0, dy: 0, gravity: 0.8, jumpPower: -12, grounded: false
        };

        const groundY = 250;
        const blocks = [
            {x: 200, y: 170, width: 40, height: 40},
            {x: 240, y: 170, width: 40, height: 40},
            {x: 380, y: 130, width: 40, height: 40}
        ];

        let keys = {};
        window.addEventListener("keydown", (e) => keys[e.code] = true);
        window.addEventListener("keyup", (e) => keys[e.code] = false);

        function update() {
            if (keys["ArrowRight"] || keys["KeyD"]) mario.dx = 4;
            else if (keys["ArrowLeft"] || keys["KeyA"]) mario.dx = -4;
            else mario.dx = 0;

            if ((keys["ArrowUp"] || keys["Space"] || keys["KeyW"]) && mario.grounded) {
                mario.dy = mario.jumpPower;
                mario.grounded = false;
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
            ctx.fillStyle = "#e75914";
            ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
            ctx.fillStyle = "#00b800";
            ctx.fillRect(0, groundY, canvas.width, 10);

            ctx.fillStyle = "#b84400";
            blocks.forEach(b => ctx.fillRect(b.x, b.y, b.width, b.height));

            ctx.fillStyle = "red";
            ctx.fillRect(mario.x, mario.y, mario.width, mario.height);
            ctx.fillStyle = "brown";
            ctx.fillRect(mario.x, mario.y, mario.width, 10);
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

components.html(mario_game_html, height=360)
