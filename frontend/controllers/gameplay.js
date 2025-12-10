// main references used:
// https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript
// https://chriscourses.com/blog/coding-collision-detection-in-javascript
// const images before canvas is created
const planeImg = new Image();
planeImg.src = "../public/img/gameplay_airplane.png";
const cloudImg = new Image();
cloudImg.src = "../public/img/cloud.png";
const birdImg = new Image();
birdImg.src = "../public/img/bird.png";
const fuelImg = new Image();
fuelImg.src = "../public/img/fuel.png";
// didn't end up using coin image, but keeping it for later
const coinImg = new Image();
coinImg.src = "../public/img/coin.png";
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
const spawnInterval = 900; // ms
// Game state (distance from back, 
// after route is selected from choose airports window)
let fuel = 100;
let distance = sessionStorage.getItem("currentGame") ?
    JSON.parse(sessionStorage.getItem("currentGame")).distance : 100; 
let running = true;
// Game running state
// Weather (up to update, need weather from previous window - airport selection)
const weatherTypes = ["Sunny", "Cloudy", "Rainy"];
const currentGame_data = sessionStorage.getItem("currentGame")
    ? JSON.parse(sessionStorage.getItem("currentGame"))
    : {};
const weather = currentGame_data.weather && weatherTypes.includes(currentGame_data.weather)
document.getElementById("weather").textContent = weather;
// Input keys
let keys = {};
document.addEventListener("keydown", (e) => keys[e.key] = true);
document.addEventListener("keyup", (e) => keys[e.key] = false);

function spawnObstacle() {
    const types = ["cloud", "bird", "fuel"];
    const type = types[Math.floor(Math.random() * types.length)];
    let img;
    if (type === "cloud") img = cloudImg;
    if (type === "bird") img = birdImg;
    if (type === "fuel") img = fuelImg;
    obstacles.push({
        type,
        img,
        x: canvas.width,
        y: Math.random() * (canvas.height - 50),
        width: type === "bird" ? 20 : type === "cloud" ? 100 : type === "fuel" ? 50 : 50,
        height: type === "bird" ? 20 : type === "cloud" ? 50 : type === "fuel" ? 50 : 50,
        speed: type === "bird" ? 5 : type === "cloud" ? 2 :  type === "fuel" ? 3 : 0
    });
}
// Collision detection - only one hit
// ref - https://chriscourses.com/blog/coding-collision-detection-in-javascript
// ref - https://developer.mozilla.org/en-US/docs/Games/Tutorials/2D_Breakout_game_pure_JavaScript/Collision_detection
// comparing object's positions and their width and height
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
    // Draw player (image is scuffed, but fine)
    ctx.drawImage(planeImg, player.x, player.y, player.width, player.height);
    if (timestamp - lastSpawn > spawnInterval) {
        spawnObstacle();
        lastSpawn = timestamp;
    }
    // Update obstacles (change to certain images - clouds, birds, etc)
    obstacles.forEach((obstacle) => {
        // obstacle movement to the left
        obstacle.x -= obstacle.speed;
        ctx.drawImage(obstacle.img, obstacle.x, obstacle.y, obstacle.width, obstacle.height);
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

// Send crashed status to backend
async function sendCrashed() {
    const currentGame = JSON.parse(localStorage.getItem("currentGame")) || JSON.parse(sessionStorage.getItem("currentGame")) || {};
    const difficulty = currentGame.difficulty || "easy";
    const totalDistance = currentGame.distance || 100;
    const distanceTraveled = totalDistance - distance;
    const percentCompleted = (distanceTraveled / totalDistance) * 100;
    const partialScore = Math.round(percentCompleted / 10); // 0-10 points based on progress
    
    try {
        const response = await fetch("http://127.0.0.1:5000/crashed", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                crashed: true,
                player_name: localStorage.getItem("playerName"),
                fuel_left: fuel.toFixed(1),
                distance_left: distance.toFixed(1),
                difficulty: difficulty,
                score: partialScore
            })
        });
        const data = await response.json();
        console.log("Crashed status sent:", data);
        
        // Store result in sessionStorage for Results page
        sessionStorage.setItem("gameResult", JSON.stringify({
            crashed: true,
            won: false,
            fuel_left: fuel.toFixed(1),
            distance_left: distance.toFixed(1),
            weather: weather
        }));
        
    } catch (err) {
        console.error("Error sending crashed status:", err);
        // Still store locally even if backend fails
        sessionStorage.setItem("gameResult", JSON.stringify({
            crashed: true,
            won: false,
            fuel_left: fuel.toFixed(1),
            distance_left: distance.toFixed(1),
            weather: weather
        }));
    }
}

// Send win/score to backend
async function sendWin() {
    const currentGame = JSON.parse(localStorage.getItem("currentGame")) || JSON.parse(sessionStorage.getItem("currentGame")) || {};
    const difficulty = currentGame.difficulty || "easy";
    
    try {
        const response = await fetch("http://127.0.0.1:5000/score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                score: Math.round(fuel), 
                player_name: localStorage.getItem("playerName"),
                won: true,
                fuel_left: fuel.toFixed(1),
                difficulty: difficulty
            })
        });
        const data = await response.json();
        console.log("Win score sent:", data);
        
        // Store result in sessionStorage for Results page
        sessionStorage.setItem("gameResult", JSON.stringify({
            crashed: false,
            won: true,
            fuel_left: fuel.toFixed(1),
            distance_left: "0",
            weather: weather
        }));
        
    } catch (err) {
        console.error("Error sending win score:", err);
        // Still store locally even if backend fails
        sessionStorage.setItem("gameResult", JSON.stringify({
            crashed: false,
            won: true,
            fuel_left: fuel.toFixed(1),
            distance_left: "0",
            weather: weather
        }));
    }
}

// Game end conditions - redirect to Results page
async function endGame() {
    running = false;
    await sendCrashed();
    window.location.href = "Results.html";
}
async function winGame() {
    running = false;
    await sendWin();
    window.location.href = "Results.html";
}
// Pause button
document.getElementById("pauseButton").addEventListener("click", () => {
    running = !running;
    if (running) requestAnimationFrame(gameLoop);
});