const API_BASE = "http://127.0.0.1:5000";

let selectedStartAirport = null;
let selectedEndAirport   = null;
let selectedWeather      = null;
let airportsData = [];

const startAirportsBody   = document.getElementById("start-airports-body");
const endAirportsBody     = document.getElementById("end-airports-body");
const selectedStartSpan   = document.getElementById("selected-start");
const selectedEndSpan     = document.getElementById("selected-end");
const distanceValue       = document.getElementById("distance-value");
const difficultyBadge     = document.getElementById("difficulty-badge");
const selectedWeatherSpan = document.getElementById("selected-weather");
const startGameBtn        = document.getElementById("start-game-btn");

const weatherButtons = document.querySelectorAll(".weather-btn");


// Load airports (plain fetch)
async function fetchAirports() {
    let json;
    try {
        const res = await fetch(API_BASE + "/airports");
        json = await res.json();
        airportsData = json.airports || [];
    } catch (e) {
        console.warn("couldn't fetch airports:", e);
        airportsData = [];
    }
    return airportsData;
}


// rough distance calc (Haversine)
// TODO: maybe move to helper?
function calculateDistanceLocal(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const p = Math.PI/180;
    const dLat = (lat2 - lat1) * p;
    const dLon = (lon2 - lon1) * p;

    const a =
        Math.sin(dLat/2) ** 2 +
        Math.cos(lat1 * p) *
        Math.cos(lat2 * p) *
        Math.sin(dLon/2) ** 2;

    return R * (2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a)));
}


function getDifficulty(km) {
    if (km < 250) return "easy";
    if (km <= 500) return "medium";
    return "hard";
}


// Put airports into table
function populateAirportTable(list, tbody, type) {
    tbody.innerHTML = "";  // reset

    // for debugging:

    for (let ap of list) {
        const code = ap.iata_code || ap.ident || "N/A";

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><input type="radio" name="${type}-airport"></td>
            <td>${code}</td>
            <td>${ap.name || ""}</td>
        `;

        // store coords on element (lazy but works)
        tr.dataset.lat  = ap.latitude  || 0;
        tr.dataset.lon  = ap.longitude || 0;
        tr.dataset.code = code;

        tr.onclick = () => {
            // highlight selection
            [...tbody.querySelectorAll("tr")].forEach(row => row.classList.remove("selected"));
            tr.classList.add("selected");

            const picked = {
                code: tr.dataset.code,
                lat : parseFloat(tr.dataset.lat),
                lon : parseFloat(tr.dataset.lon)
            };

            if (type === "start") {
                selectedStartAirport = picked;
                selectedStartSpan.textContent = picked.code;
            } else {
                selectedEndAirport = picked;
                selectedEndSpan.textContent = picked.code;
            }

            if (selectedStartAirport && selectedEndAirport) {
                refreshDistanceUI();
            }

            updateStartButtonState();
        };

        tbody.appendChild(tr);
    }
}


// small helper to recompute & display distance + difficulty
function refreshDistanceUI() {
    if (!selectedStartAirport || !selectedEndAirport) return;

    const km = calculateDistanceLocal(
        selectedStartAirport.lat, selectedStartAirport.lon,
        selectedEndAirport.lat,   selectedEndAirport.lon
    );

    distanceValue.textContent = km.toFixed(2);
    updateDifficultyBadge(getDifficulty(km));
}


// color box for difficulty
function updateDifficultyBadge(d) {
    difficultyBadge.textContent = d || "--";
    difficultyBadge.className = "difficulty-badge " + d;
}


// weather choice
weatherButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        weatherButtons.forEach(b => b.classList.remove("selected"));
        btn.classList.add("selected");

        selectedWeather = btn.dataset.weather;
        selectedWeatherSpan.textContent =
            selectedWeather[0].toUpperCase() + selectedWeather.slice(1);

        updateStartButtonState();
    });
});

// Enable button only when everything is selected
function updateStartButtonState() {
    startGameBtn.disabled =
        !(selectedStartAirport && selectedEndAirport && selectedWeather);
}

// used to also store difficulty
function getCurrentDistanceAndDifficulty() {
    if (!selectedStartAirport || !selectedEndAirport) {
        return { km: 0, difficulty: "easy" };
    }
    const km = calculateDistanceLocal(
        selectedStartAirport.lat,
        selectedStartAirport.lon,
        selectedEndAirport.lat,
        selectedEndAirport.lon
    );
    return { km, difficulty: getDifficulty(km) };
}


// Button start game
startGameBtn.onclick = async () => {
    if (!selectedStartAirport || !selectedEndAirport || !selectedWeather) {
        alert("Select everything first.");
        return;
    }
    let playerName =
        sessionStorage.getItem("selectedPlayer") ||
        localStorage.getItem("playerName");
    if (!playerName) {
        playerName = prompt("Enter player name:");
        if (!playerName) return;
        localStorage.setItem("playerName", playerName);
        sessionStorage.setItem("playerName", playerName);
    } else {
        // keep storage consistent (just in case)
        localStorage.setItem("playerName", playerName);
    }

    const { km, difficulty } = getCurrentDistanceAndDifficulty();
    // send basic game info to backend (if fails, just continue)
    try {
        await fetch(API_BASE + "/save_game", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                player_name   : playerName,
                start_airport : selectedStartAirport.code,
                ending_airport: selectedEndAirport.code,
                weather       : selectedWeather
            })
        });
    } catch (err) {
        console.log("save_game failed (not fatal):", err);
    }
    const gameData = {
        startAirport : selectedStartAirport.code,
        endAirport   : selectedEndAirport.code,
        weather      : selectedWeather,
        distance     : km,
        difficulty
    };

    // store for gameplay.js
    sessionStorage.setItem("currentGame", JSON.stringify(gameData));
    localStorage.setItem("currentGame", JSON.stringify(gameData));
    window.location.href = "gameplay.html";
};

// Page init
async function init() {
    const ap = await fetchAirports();
    if (ap.length) {
        populateAirportTable(ap, startAirportsBody, "start");
        populateAirportTable(ap, endAirportsBody, "end");
    } else {
        startAirportsBody.innerHTML = "<tr><td colspan='3'>No airports found</td></tr>";
        endAirportsBody.innerHTML   = "<tr><td colspan='3'>No airports found</td></tr>";
    }
}
// a bit redundant but harmless
document.addEventListener("DOMContentLoaded", init);
