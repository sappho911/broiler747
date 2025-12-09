// main reference used:
// https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript

// const images before canvas is created



// canvas, player, obstacles setup
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const player = {
    x: 100,
    y: 200,
    width: 40,
    height: 40,
    speed: 4
};
let obstacles = [];
let lastSpawn = 0;
const spawnInterval = 1200; // ms

// Game state (not done, need to add fuel and distance from back, 
// after route is selected from choose airports window)
let fuel = 100;
let distance = 100;
// Game running state
let running = true;
// Weather (up to update, need weather from previous window - airport selection)
const weatherTypes = ["Sunny", "Cloudy", "Rainy"];
const weather = weatherTypes[Math.floor(Math.random() * weatherTypes.length)];
document.getElementById("weather").textContent = weather;

// Input keys
let keys = {};
document.addEventListener("keydown", (e) => keys[e.key] = true);
document.addEventListener("keyup", (e) => keys[e.key] = false);

function spawnObstacle() {
    obstacles.push({
        x: canvas.width,
        y: Math.random() * (canvas.height - 40),
        width: 40,
        height: 40,
        speed: weather === "Rainy" ? 5 : 3
    });
}
// Collision detection - only one hit
// ref - https://chriscourses.com/blog/coding-collision-detection-in-javascript
// ref - https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Collision_detection
// comparing object positons and their width and height
function rectCollision(a, b) {
    return (
        a.x < b.x + b.width && a.x + a.width > b.x &&
        a.y < b.y + b.height && a.y + a.height > b.y
    );
}
// Main Game loop
let lastTime = 0;
function gameLoop(timestamp) {
    if (!running) return;
    const delta = timestamp - lastTime;
    lastTime = timestamp;
    // Clear screen
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Background (different gifs are uploaded here, for now colors)
    if (weather === "Cloudy") {
        ctx.fillStyle = "#cce";
    } else if (weather === "Rainy") {
        ctx.fillStyle = "#99a";
    } else {
        ctx.fillStyle = "#aee";
    }
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    // Player movement
    if (keys["ArrowUp"] && player.y > 0) player.y -= player.speed;
    if (keys["ArrowDown"] && player.y < canvas.height - player.height) player.y += player.speed;
    // Draw player (change to images, instead of rect drawImage)
    ctx.fillStyle = "yellow";
    ctx.fillRect(player.x, player.y, player.width, player.height);
    if (timestamp - lastSpawn > spawnInterval) {
        spawnObstacle();
        lastSpawn = timestamp;
    }
    // Update obstacles (change to certain images - clouds, birds, etc)
    obstacles.forEach((obstacle) => {
        obstacle.x -= obstacle.speed;
        ctx.fillStyle = "red";
        ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
        if (rectCollision(player, obstacle)) {
            endGame();
        }
    });
    // Remove off-screen obstacles
    obstacles = obstacles.filter(obst => obst.x + obst.width > 0);
    // Fuel + distance - up to debate what are values here 
    // + consider fuel barrels taken upon collision
    fuel -= 0.01;
    distance -= 0.05;
    document.getElementById("fuel").textContent = fuel.toFixed(1);
    document.getElementById("distance").textContent = distance.toFixed(1);
    if (fuel <= 0) endGame();
    if (distance <= 0) winGame();
    // requestAnimationFrame to create an animation loop
    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);
// Game end conditions, for now alerts and redirect
// also need to store score data to push it further to next final results window and to backend
function endGame() {
    running = false;
    alert("Crashed! Moving to quiz...");
    window.location.href = "quiz.html";
}
function winGame() {
    running = false;
    alert("Arrived! Moving to quiz...");
    window.location.href = "quiz.html";
}

// Pause button
document.getElementById("pauseButton").addEventListener("click", () => {
    running = !running;
    if (running) requestAnimationFrame(gameLoop);
});