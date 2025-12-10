
const API_BASE = "http://127.0.0.1:5000";

// State
let selectedStartAirport = null;
let selectedEndAirport = null;
let selectedWeather = null;
let airportsData = []; 
const startAirportsBody = document.getElementById("start-airports-body");
const endAirportsBody = document.getElementById("end-airports-body");
const selectedStartSpan = document.getElementById("selected-start");
const selectedEndSpan = document.getElementById("selected-end");
const distanceValue = document.getElementById("distance-value");
const difficultyBadge = document.getElementById("difficulty-badge");
const selectedWeatherSpan = document.getElementById("selected-weather");
const startGameBtn = document.getElementById("start-game-btn");
const weatherButtons = document.querySelectorAll(".weather-btn");

async function fetchAirports() {
    try {
        const response = await fetch(`${API_BASE}/airports`);
        const data = await response.json();
        airportsData = data.airports || [];
        return airportsData;
    } catch (error) {
        console.error("Error fetching airports:", error);
        return [];
    }
}
// Haversine formula to calculate distance between two lat/lon points
function calculateDistanceLocal(lat1, lon1, lat2, lon2) {
    const R = 6371; const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

function getDifficulty(distanceKm) {
    if (distanceKm < 250) return "easy";
    if (distanceKm <= 500) return "medium";
    return "hard";
}
function populateAirportTable(airports, tbody, type) {
    tbody.innerHTML = "";
    
    airports.forEach((airport) => {
        const row = document.createElement("tr");
        const airportCode = airport.iata_code || airport.ident || "N/A";
        row.innerHTML = `
            <td><input type="radio" name="${type}-airport" value="${airportCode}"></td>
            <td>${airportCode}</td>
            <td>${airport.name || "Unknown"}</td>
        `;
        
        row.dataset.lat = airport.latitude || 0;
        row.dataset.lon = airport.longitude || 0;
        row.dataset.code = airportCode;
        
        row.addEventListener("click", () => {
            const radio = row.querySelector('input[type="radio"]');
            radio.checked = true;
            tbody.querySelectorAll("tr").forEach(r => r.classList.remove("selected"));
            row.classList.add("selected");
            
            if (type === "start") {
                selectedStartAirport = {
                    code: airportCode,
                    lat: parseFloat(row.dataset.lat),
                    lon: parseFloat(row.dataset.lon)
                };
                selectedStartSpan.textContent = airportCode;
            } else {
                selectedEndAirport = {
                    code: airportCode,
                    lat: parseFloat(row.dataset.lat),
                    lon: parseFloat(row.dataset.lon)
                };
                selectedEndSpan.textContent = airportCode;
            }
            
            if (selectedStartAirport && selectedEndAirport) {
                calculateDistance();
            }
            
            checkCanStartGame();
        });
        
        tbody.appendChild(row);
    });
}
function calculateDistance() {
    if (!selectedStartAirport || !selectedEndAirport) return;
    
    const km = calculateDistanceLocal(
        selectedStartAirport.lat,
        selectedStartAirport.lon,
        selectedEndAirport.lat,
        selectedEndAirport.lon
    );
    
    const difficulty = getDifficulty(km);
    
    distanceValue.textContent = km.toFixed(2);
    updateDifficultyBadge(difficulty);
}

function updateDifficultyBadge(difficulty) {
    difficultyBadge.textContent = difficulty || "--";
    difficultyBadge.className = "difficulty-badge";
    
    if (difficulty === "easy") {
        difficultyBadge.classList.add("easy");
    } else if (difficulty === "medium") {
        difficultyBadge.classList.add("medium");
    } else if (difficulty === "hard") {
        difficultyBadge.classList.add("hard");
    }
}

weatherButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        weatherButtons.forEach(b => b.classList.remove("selected"));
        btn.classList.add("selected");
        
        selectedWeather = btn.dataset.weather;
        selectedWeatherSpan.textContent = selectedWeather.charAt(0).toUpperCase() + selectedWeather.slice(1);
        
        checkCanStartGame();
    });
});
function checkCanStartGame() {
    if (selectedStartAirport && selectedEndAirport && selectedWeather) {
        startGameBtn.disabled = false;
    } else {
        startGameBtn.disabled = true;
    }
}

function getCurrentDistanceAndDifficulty() {
    if (!selectedStartAirport || !selectedEndAirport) return { km: 0, difficulty: "easy" };
    const km = calculateDistanceLocal(
        selectedStartAirport.lat,
        selectedStartAirport.lon,
        selectedEndAirport.lat,
        selectedEndAirport.lon
    );
    return { km: km, difficulty: getDifficulty(km) };
}
startGameBtn.addEventListener("click", async () => {
    if (!selectedStartAirport || !selectedEndAirport || !selectedWeather) {
        alert("Please select start airport, end airport, and weather!");
        return;
    }
    
    let playerName = sessionStorage.getItem("selectedPlayer") || localStorage.getItem("playerName");
    if (!playerName) {
        playerName = prompt("Enter your player name:");
        if (playerName) {
            localStorage.setItem("playerName", playerName);
            sessionStorage.setItem("playerName", playerName);
        } else {
            alert("Player name is required!");
            return;
        }
    } else {
        // Make sure it's in localStorage for gameplay.js
        localStorage.setItem("playerName", playerName);
    }
    
    const { km, difficulty } = getCurrentDistanceAndDifficulty();
    
    try {
        const response = await fetch(`${API_BASE}/save_game`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                player_name: playerName,
                start_airport: selectedStartAirport.code,
                ending_airport: selectedEndAirport.code,
                weather: selectedWeather
            })
        });
        
        const data = await response.json();
        
        const gameData = {
            startAirport: selectedStartAirport.code,
            endAirport: selectedEndAirport.code,
            weather: selectedWeather,
            distance: km,
            difficulty: difficulty
        };
        sessionStorage.setItem("currentGame", JSON.stringify(gameData));
        localStorage.setItem("currentGame", JSON.stringify(gameData));
        
        window.location.href = "gameplay.html";
    } catch (error) {
        console.error("Error starting game:", error);
        const gameData = {
            startAirport: selectedStartAirport.code,
            endAirport: selectedEndAirport.code,
            weather: selectedWeather,
            distance: km,
            difficulty: difficulty
        };
        sessionStorage.setItem("currentGame", JSON.stringify(gameData));
        localStorage.setItem("currentGame", JSON.stringify(gameData));
        window.location.href = "gameplay.html";
    }
});
async function init() {
    const airports = await fetchAirports();
    
    if (airports.length > 0) {
        populateAirportTable(airports, startAirportsBody, "start");
        populateAirportTable(airports, endAirportsBody, "end");
    } else {
        startAirportsBody.innerHTML = '<tr><td colspan="3">No airports found</td></tr>';
        endAirportsBody.innerHTML = '<tr><td colspan="3">No airports found</td></tr>';
    }
}

document.addEventListener("DOMContentLoaded", init);