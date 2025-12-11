document.addEventListener("DOMContentLoaded", () => {
    const gameResultSession = JSON.parse(sessionStorage.getItem("gameResult")) || {};
    const currentGameLocal = JSON.parse(localStorage.getItem("currentGame")) || {};
    const currentGameSession = JSON.parse(sessionStorage.getItem("currentGame")) || {};
    const gameResult = gameResultSession;
    const currentGame = { ...currentGameLocal, ...currentGameSession };
    const playerName = localStorage.getItem("playerName") || sessionStorage.getItem("playerName") || "Unknown";

    console.log("gameResult:", gameResult);
    console.log("currentGame:", currentGame);
    console.log("playerName:", playerName);
    const resultTitle = document.getElementById("result-title");
    const playerNameEl = document.getElementById("player-name");
    const gameStatusEl = document.getElementById("game-status");
    const startAirportEl = document.getElementById("start-airport");
    const endAirportEl = document.getElementById("end-airport");
    const weatherEl = document.getElementById("weather");
    const totalDistanceEl = document.getElementById("total-distance");
    const distanceLeftEl = document.getElementById("distance-left");
    const fuelLeftEl = document.getElementById("fuel-left");
    const difficultyEl = document.getElementById("difficulty");
    
    playerNameEl.textContent = playerName;
    if (gameResult.crashed) {
        resultTitle.textContent = "CRASHED!";
        resultTitle.classList.add("crashed");
        gameStatusEl.textContent = "Crashed";
        gameStatusEl.classList.add("status-crashed");
    } else if (gameResult.won) {
        resultTitle.textContent = "YOU WIN!";
        resultTitle.classList.add("won");
        gameStatusEl.textContent = "Arrived Safely!";
        gameStatusEl.classList.add("status-won");
    } else {
        resultTitle.textContent = "GAME OVER";
        gameStatusEl.textContent = "Unknown";
    }
    
    startAirportEl.textContent = currentGame.startAirport || currentGame.start_airport || "--";
    endAirportEl.textContent = currentGame.endAirport || currentGame.end_airport || "--";
    weatherEl.textContent = currentGame.weather || gameResult.weather || "--";
    
    const totalDist = currentGame.distance;
    if (totalDist) {
        totalDistanceEl.textContent = typeof totalDist === 'number' ? `${totalDist.toFixed(2)} km` : `${totalDist} km`;
    } else {
        totalDistanceEl.textContent = "--";
    }
    
    distanceLeftEl.textContent = gameResult.distance_left ? `${gameResult.distance_left} km` : "0 km";
    fuelLeftEl.textContent = gameResult.fuel_left ? `${gameResult.fuel_left}%` : "0%";

    const difficulty = currentGame.difficulty || "--";
    difficultyEl.textContent = typeof difficulty === 'string' ? difficulty.toUpperCase() : difficulty;
    if (difficulty === "easy") {
        difficultyEl.classList.add("easy");
    } else if (difficulty === "medium") {
        difficultyEl.classList.add("medium");
    } else if (difficulty === "hard") {
        difficultyEl.classList.add("hard");
    }
    
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
