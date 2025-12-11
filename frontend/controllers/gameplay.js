// basic image setup (just loading everything here)
const planeImg = new Image();
planeImg.src = "../public/img/gameplay_airplane.png";

const cloudImg = new Image();
cloudImg.src = "../public/img/cloud.png";

const birdImg = new Image();
birdImg.src = "../public/img/bird.png";

const fuelImg = new Image();
fuelImg.src = "../public/img/fuel.png";

const coinImg = new Image(); // might use later
coinImg.src = "../public/img/coin.png";

// canvas stuff
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// very basic player object
const player = {
    x: 100,
    y: 200,
    width: 40,
    height: 40,
    speed: 4
};

let obstacles = [];
let lastSpawn = 0;
const spawnInterval = 900; // ms between obstacles

// game state (taken from previous page)
const savedGame = sessionStorage.getItem("currentGame")
    ? JSON.parse(sessionStorage.getItem("currentGame"))
    : {};

let fuel = 100;
let distance = savedGame.distance || 100;
let running = true;
// weather coming from previous window
let weather = savedGame.weather || "Sunny";
document.getElementById("weather").textContent = weather;
// key inputs
let keys = {};
document.addEventListener("keydown", e => keys[e.key] = true);
document.addEventListener("keyup", e => keys[e.key] = false);

// random obstacle
function spawnObstacle() {
    const choice = ["cloud", "bird", "fuel"];
    const type = choice[Math.floor(Math.random() * choice.length)];
    let img;
    let size = { w: 50, h: 50 };
    let speed = 3;
    if (type === "cloud") {
        img = cloudImg;
        size = { w: 100, h: 50 };
        speed = 2;
    } else if (type === "bird") {
        img = birdImg;
        size = { w: 20, h: 20 };
        speed = 5;
    } else {
        img = fuelImg;
    }
    obstacles.push({
        type,
        img,
        x: canvas.width,
        y: Math.random() * (canvas.height - size.h),
        width: size.w,
        height: size.h,
        speed
    });
}
// dumb but reliable collision detection
function rectCollision(a, b) {
    return (
        a.x < b.x + b.width &&
        a.x + a.width > b.x &&
        a.y < b.y + b.height &&
        a.y + a.height > b.y
    );
}
// core loop
let lastTime = 0;
function gameLoop(ts) {
    if (!running) return;
    const dt = ts - lastTime;
    lastTime = ts;
    // background depending on weather, temporary colors
    if (weather === "Cloudy") ctx.fillStyle = "#cce";
    else if (weather === "Rainy") ctx.fillStyle = "#99a";
    else ctx.fillStyle = "#aee";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    // player movement
    if (keys["ArrowUp"] && player.y > 0) player.y -= player.speed;
    if (keys["ArrowDown"] && player.y < canvas.height - player.height) player.y += player.speed;
    // draw airplane
    ctx.drawImage(planeImg, player.x, player.y, player.width, player.height);
    // spawn new obstacles occasionally
    if (ts - lastSpawn > spawnInterval) {
        spawnObstacle();
        lastSpawn = ts;
    }

    // update all obstacles
    obstacles.forEach(o => {
        o.x -= o.speed;
        ctx.drawImage(o.img, o.x, o.y, o.width, o.height);
        // if we hit something -> game ends
        if (rectCollision(player, o)) {
            endGame();
        }
    });

    // remove those that moved left off screen
    obstacles = obstacles.filter(o => o.x + o.width > 0);
    // fuel + distance decrease
    fuel -= 0.01;
    distance -= 0.05;

    document.getElementById("fuel").textContent = fuel.toFixed(1);
    document.getElementById("distance").textContent = distance.toFixed(1);

    if (fuel <= 0) endGame();
    if (distance <= 0) winGame();

    requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);

// crash event
async function sendCrashed() {
    const name = localStorage.getItem("playerName");
    const total = savedGame.distance || 100;

    const traveled = total - distance;
    const part = Math.round((traveled / total) * 10);

    try {
        await fetch("http://127.0.0.1:5000/crashed", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                crashed: true,
                player_name: name,
                fuel_left: fuel.toFixed(1),
                distance_left: distance.toFixed(1),
                difficulty: savedGame.difficulty || "easy",
                score: part
            })
        });
    } catch (e) {
        console.log("Couldn't send crash info:", e);
    }
    // still store result locally
    sessionStorage.setItem("gameResult", JSON.stringify({
        crashed: true,
        won: false,
        fuel_left: fuel.toFixed(1),
        distance_left: distance.toFixed(1),
        weather
    }));
}
// win event
async function sendWin() {
    const name = localStorage.getItem("playerName");
    try {
        await fetch("http://127.0.0.1:5000/score", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                score: Math.round(fuel),
                player_name: name,
                won: true,
                fuel_left: fuel.toFixed(1),
                difficulty: savedGame.difficulty || "easy"
            })
        });
    } catch (e) {
        console.log("Couldn't send win info:", e);
    }

    sessionStorage.setItem("gameResult", JSON.stringify({
        crashed: false,
        won: true,
        fuel_left: fuel.toFixed(1),
        distance_left: "0",
        weather
    }));
}
// redirecting
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
// pause
document.getElementById("pauseButton").addEventListener("click", () => {
    running = !running;
    if (running) requestAnimationFrame(gameLoop);
});
