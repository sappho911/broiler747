document.addEventListener("DOMContentLoaded", () => {
    // grab everything we might need
    const gameRes = JSON.parse(sessionStorage.getItem("gameResult")) || {};
    const gameLocal = JSON.parse(localStorage.getItem("currentGame")) || {};
    const gameSession = JSON.parse(sessionStorage.getItem("currentGame")) || {};
    const game = { ...gameLocal, ...gameSession };

    const playerName =
        localStorage.getItem("playerName") ||
        sessionStorage.getItem("playerName") ||
        "Unknown";

    console.log("gameResult:", gameRes);
    console.log("game:", game);
    console.log("player:", playerName);

    // elements
    const titleEl = document.getElementById("result-title");
    const nameEl = document.getElementById("player-name");
    const statusEl = document.getElementById("game-status");
    const startEl = document.getElementById("start-airport");
    const endEl = document.getElementById("end-airport");
    const weatherEl = document.getElementById("weather");
    const totalDistEl = document.getElementById("total-distance");
    const leftDistEl = document.getElementById("distance-left");
    const fuelEl = document.getElementById("fuel-left");
    const diffEl = document.getElementById("difficulty");

    // fill in name
    nameEl.textContent = playerName;

    // crashed / won text
    if (gameRes.crashed) {
        titleEl.textContent = "CRASHED!";
        titleEl.classList.add("crashed");

        statusEl.textContent = "Crashed";
        statusEl.classList.add("status-crashed");

    } else if (gameRes.won) {
        titleEl.textContent = "YOU WIN!";
        titleEl.classList.add("won");

        statusEl.textContent = "Arrived Safely!";
        statusEl.classList.add("status-won");

    } else {
        titleEl.textContent = "GAME OVER";
        statusEl.textContent = "Unknown";
    }

    // airports + weather
    startEl.textContent = game.startAirport || game.start_airport || "--";
    endEl.textContent = game.endAirport || game.end_airport || "--";
    weatherEl.textContent = game.weather || gameRes.weather || "--";

    // distance
    if (game.distance) {
        totalDistEl.textContent =
            typeof game.distance === "number"
                ? `${game.distance.toFixed(2)} km`
                : `${game.distance} km`;
    } else {
        totalDistEl.textContent = "--";
    }

    leftDistEl.textContent = gameRes.distance_left
        ? `${gameRes.distance_left} km`
        : "0 km";

    fuelEl.textContent = gameRes.fuel_left
        ? `${gameRes.fuel_left}%`
        : "0%";

    // difficulty coloring
    const diff = game.difficulty || "--";
    diffEl.textContent = typeof diff === "string" ? diff.toUpperCase() : diff;

    if (diff === "easy") diffEl.classList.add("easy");
    if (diff === "medium") diffEl.classList.add("medium");
    if (diff === "hard") diffEl.classList.add("hard");

    // buttons
    document.getElementById("quiz-btn").addEventListener("click", () => {
        window.location.href = "quiz.html";
    });

    document.getElementById("play-again-btn").addEventListener("click", () => {
        sessionStorage.removeItem("gameResult");
        window.location.href = "new_game.html";
    });

    document.getElementById("main-menu-btn").addEventListener("click", () => {
        sessionStorage.removeItem("gameResult");
        window.location.href = "main_menu.html";
    });
});
