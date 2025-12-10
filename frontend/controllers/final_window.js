// Final Window Controller - Display final score and game summary

document.addEventListener("DOMContentLoaded", () => {
    // Get ALL data from BOTH storages
    const quizScore = JSON.parse(sessionStorage.getItem("quizScore")) || { score: 0, total: 5 };
    const gameResult = JSON.parse(sessionStorage.getItem("gameResult")) || {};
    const currentGameLocal = JSON.parse(localStorage.getItem("currentGame")) || {};
    const currentGameSession = JSON.parse(sessionStorage.getItem("currentGame")) || {};
    const currentGame = { ...currentGameLocal, ...currentGameSession };
    const playerName = localStorage.getItem("playerName") || sessionStorage.getItem("playerName") || "Unknown";
    
    console.log("quizScore:", quizScore);
    console.log("gameResult:", gameResult);
    console.log("currentGame:", currentGame);
    console.log("playerName:", playerName);
    
    const difficulty = currentGame.difficulty || "easy";
    let difficultyMultiplier = 1;
    if (difficulty === "medium") {
        difficultyMultiplier = 1.5;
    } else if (difficulty === "hard") {
        difficultyMultiplier = 2;
    }
    
    const totalDistance = parseFloat(currentGame.distance) || 100;
    const distanceLeft = parseFloat(gameResult.distance_left) || 0;
    const distanceTraveled = totalDistance - distanceLeft;
    const percentCompleted = (distanceTraveled / totalDistance) * 100;
    
    let baseTravelScore = 0;
    if (gameResult.won) {
        baseTravelScore = 5; //
    } else if (gameResult.crashed) {
        baseTravelScore = (percentCompleted / 100) * 5;
    }
    
    const travelScore = Math.round(baseTravelScore * difficultyMultiplier * 10) / 10;
    const maxTravelScore = Math.round(5 * difficultyMultiplier * 10) / 10;
    
    const quizPoints = quizScore.score || 0;
    const totalScore = Math.round((quizPoints + travelScore) * 10) / 10;
    const maxTotalScore = 5 + maxTravelScore;
    
    console.log("Difficulty:", difficulty, "Multiplier:", difficultyMultiplier);
    console.log("Distance Traveled:", distanceTraveled, "/", totalDistance, "=", percentCompleted.toFixed(1), "%");
    console.log("Travel Score:", travelScore, "/", maxTravelScore, "Quiz Score:", quizPoints, "Total:", totalScore, "/", maxTotalScore);
    
    const titleEl = document.getElementById("final_score_title");
    const playerNameEl = document.getElementById("player-name");
    const gameStatusEl = document.getElementById("game-status");
    const startAirportEl = document.getElementById("start-airport");
    const endAirportEl = document.getElementById("end-airport");
    const weatherEl = document.getElementById("weather");
    const totalDistanceEl = document.getElementById("total-distance");
    const distanceTraveledEl = document.getElementById("distance-traveled");
    const distanceLeftEl = document.getElementById("distance-left");
    const fuelLeftEl = document.getElementById("fuel-left");
    const difficultyEl = document.getElementById("difficulty");
    const difficultyBonusEl = document.getElementById("difficulty-bonus");
    const scoreValueEl = document.getElementById("final_score_value");
    const travelScoreEl = document.getElementById("travel-score");
    const totalScoreEl = document.getElementById("total-score");
    
    if (playerNameEl) playerNameEl.textContent = playerName;
    
    if (gameResult.crashed) {
        if (titleEl) {
            titleEl.textContent = "CRASHED!";
            titleEl.classList.add("crashed");
        }
        if (gameStatusEl) {
            gameStatusEl.textContent = "Crashed";
            gameStatusEl.classList.add("status-crashed");
        }
    } else if (gameResult.won) {
        if (titleEl) {
            titleEl.textContent = "YOU WIN!";
            titleEl.classList.add("won");
        }
        if (gameStatusEl) {
            gameStatusEl.textContent = "Arrived Safely!";
            gameStatusEl.classList.add("status-won");
        }
    } else {
        if (gameStatusEl) gameStatusEl.textContent = "Unknown";
    }
    
    if (startAirportEl) startAirportEl.textContent = currentGame.startAirport || currentGame.start_airport || "--";
    if (endAirportEl) endAirportEl.textContent = currentGame.endAirport || currentGame.end_airport || "--";
    if (weatherEl) weatherEl.textContent = currentGame.weather || gameResult.weather || "--";
    
    if (totalDistanceEl) {
        if (totalDistance) {
            totalDistanceEl.textContent = `${totalDistance.toFixed(2)} km`;
        } else {
            totalDistanceEl.textContent = "--";
        }
    }
    
    if (distanceTraveledEl) {
        distanceTraveledEl.textContent = `${distanceTraveled.toFixed(2)} km (${percentCompleted.toFixed(0)}%)`;
    }
    
    if (distanceLeftEl) distanceLeftEl.textContent = gameResult.distance_left ? `${gameResult.distance_left} km` : "0 km";
    if (fuelLeftEl) fuelLeftEl.textContent = gameResult.fuel_left ? `${gameResult.fuel_left}%` : "0%";
    
    if (difficultyEl) {
        difficultyEl.textContent = typeof difficulty === 'string' ? difficulty.toUpperCase() : difficulty;
        if (difficulty === "easy") {
            difficultyEl.classList.add("easy");
        } else if (difficulty === "medium") {
            difficultyEl.classList.add("medium");
        } else if (difficulty === "hard") {
            difficultyEl.classList.add("hard");
        }
    }
    
    if (difficultyBonusEl) {
        if (difficulty === "easy") {
            difficultyBonusEl.textContent = "1x (no bonus)";
            difficultyBonusEl.classList.add("easy");
        } else if (difficulty === "medium") {
            difficultyBonusEl.textContent = "1.5x bonus";
            difficultyBonusEl.classList.add("medium");
        } else if (difficulty === "hard") {
            difficultyBonusEl.textContent = "2x bonus";
            difficultyBonusEl.classList.add("hard");
        }
    }
    
    if (scoreValueEl) {
        scoreValueEl.textContent = `${quizPoints} / 5`;
    }
    if (travelScoreEl) {
        travelScoreEl.textContent = `${travelScore} / ${maxTravelScore}`;
    }
    if (totalScoreEl) {
        totalScoreEl.textContent = `${totalScore} / ${maxTotalScore}`;
    }
    
    sendFinalScore(playerName, difficulty, totalScore);
    
    document.getElementById("play-again-btn")?.addEventListener("click", () => {
        sessionStorage.removeItem("gameResult");
        sessionStorage.removeItem("quizScore");
        window.location.href = "new_game.html";
    });
    
    document.getElementById("back_to_menu_btn")?.addEventListener("click", () => {
        sessionStorage.removeItem("gameResult");
        sessionStorage.removeItem("quizScore");
        window.location.href = "main_menu.html";
    });
});
async function sendFinalScore(playerName, difficulty, totalScore) {
    if (!playerName || !difficulty) {
        console.log("Missing player name or difficulty, skipping score update");
        return;
    }
    
    try {
        const response = await fetch("http://127.0.0.1:5000/update_final_score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                player_name: playerName,
                difficulty: difficulty,
                score: Math.round(totalScore)
            })
        });
        const data = await response.json();
        console.log("Final score sent:", data);
    } catch (err) {
        console.error("Error sending final score:", err);
    }
}