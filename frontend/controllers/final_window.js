// Final screen controller – shows summary + final score

document.addEventListener("DOMContentLoaded", () => {
    // pulling everything from storage (local + session, whichever exists)
    const quizScore = JSON.parse(sessionStorage.getItem("quizScore")) || { score: 0, total: 5 };
    const gameResult = JSON.parse(sessionStorage.getItem("gameResult")) || {};

    // current game is sometimes stored in both, so just merge them
    const storedLocal = JSON.parse(localStorage.getItem("currentGame")) || {};
    const storedSession = JSON.parse(sessionStorage.getItem("currentGame")) || {};
    const currentGame = { ...storedLocal, ...storedSession };

    const playerName = localStorage.getItem("playerName") 
        || sessionStorage.getItem("playerName") 
        || "Unknown Player";

    // debug prints (leaving them for dev)
    console.log("quiz:", quizScore);
    console.log("result:", gameResult);
    console.log("game:", currentGame);

    // difficulty rules
    const difficulty = currentGame.difficulty || "easy";
    let diffMult = 1;
    if (difficulty === "medium") diffMult = 1.5;
    else if (difficulty === "hard") diffMult = 2;

    // distance-based scoring
    const totalDist = parseFloat(currentGame.distance) || 100;
    const distLeft = parseFloat(gameResult.distance_left) || 0;
    const distDone = totalDist - distLeft;
    const percent = (distDone / totalDist) * 100;

    // travel scoring logic
    let baseScore = 0;
    if (gameResult.won) {
        baseScore = 5;
    } else if (gameResult.crashed) {
        baseScore = (percent / 100) * 5;
    }

    const travelScore = Math.round(baseScore * diffMult * 10) / 10;
    const maxTravel = Math.round(5 * diffMult * 10) / 10;
    const quizPoints = quizScore.score || 0;
    const totalScore = Math.round((quizPoints + travelScore) * 10) / 10;
    const maxTotal = 5 + maxTravel;

    // UI bindings
    const titleEl = document.getElementById("final_score_title");
    const nameEl = document.getElementById("player-name");
    const statusEl = document.getElementById("game-status");
    if (nameEl) nameEl.textContent = playerName;

    // crashed / win text
    if (gameResult.crashed) {
        titleEl && (titleEl.textContent = "CRASHED!");
        titleEl && titleEl.classList.add("crashed");
        statusEl && (statusEl.textContent = "Crashed");
        statusEl && statusEl.classList.add("status-crashed");
    } else if (gameResult.won) {
        titleEl && (titleEl.textContent = "YOU WIN!");
        titleEl && titleEl.classList.add("won");
        statusEl && (statusEl.textContent = "Arrived Safely!");
        statusEl && statusEl.classList.add("status-won");
    } else {
        statusEl && (statusEl.textContent = "Unknown");
    }

    // route + weather
    const startEl = document.getElementById("start-airport");
    const endEl = document.getElementById("end-airport");
    const weatherEl = document.getElementById("weather");
    startEl && (startEl.textContent = currentGame.startAirport || currentGame.start_airport || "--");
    endEl && (endEl.textContent = currentGame.endAirport || currentGame.end_airport || "--");
    weatherEl && (weatherEl.textContent = currentGame.weather || gameResult.weather || "--");

    // distances / fuel
    const totalDistEl = document.getElementById("total-distance");
    const distDoneEl = document.getElementById("distance-traveled");
    const distLeftEl = document.getElementById("distance-left");
    const fuelEl = document.getElementById("fuel-left");
    totalDistEl && (totalDistEl.textContent = `${totalDist.toFixed(2)} km`);
    distDoneEl && (distDoneEl.textContent = `${distDone.toFixed(2)} km (${percent.toFixed(0)}%)`);
    distLeftEl && (distLeftEl.textContent = (gameResult.distance_left || 0) + " km");
    fuelEl && (fuelEl.textContent = (gameResult.fuel_left || "0") + "%");

    // difficulty stuff
    const diffEl = document.getElementById("difficulty");
    const diffBonusEl = document.getElementById("difficulty-bonus");
    if (diffEl) {
        diffEl.textContent = difficulty.toUpperCase();
        diffEl.classList.add(difficulty);
    }
    if (diffBonusEl) {
        if (difficulty === "easy") {
            diffBonusEl.textContent = "1x (no bonus)";
        } else if (difficulty === "medium") {
            diffBonusEl.textContent = "1.5x bonus";
        } else {
            diffBonusEl.textContent = "2x bonus";
        }
        diffBonusEl.classList.add(difficulty);
    }

    // scores
    const scoreQuizEl = document.getElementById("final_score_value");
    const travelEl = document.getElementById("travel-score");
    const totalEl = document.getElementById("total-score");
    scoreQuizEl && (scoreQuizEl.textContent = `${quizPoints} / 5`);
    travelEl && (travelEl.textContent = `${travelScore} / ${maxTravel}`);
    totalEl && (totalEl.textContent = `${totalScore} / ${maxTotal}`);
    // send summary to backend
    sendFinalScore(playerName, difficulty, totalScore);

    // UI buttons
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


// send final combined score to backend
async function sendFinalScore(playerName, difficulty, totalScore) {

    if (!playerName || !difficulty) {
        console.log("Missing player info, not sending final score.");
        return;
    }
    try {
        const res = await fetch("http://127.0.0.1:5000/update_final_score", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                player_name: playerName,
                difficulty,
                score: Math.round(totalScore)
            })
        });
        const data = await res.json();
        console.log("Final score updated:", data);

    } catch (err) {
        console.log("Failed sending final score:", err);
    }
}
