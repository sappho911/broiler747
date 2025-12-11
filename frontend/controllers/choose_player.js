import { getPlayers } from "../model/players.js";

document.addEventListener("DOMContentLoaded", async () => {
    // try to load players from backend
    let players = [];
    try {
        players = await getPlayers();
        renderPlayerList(players);
    } catch (err) {
        console.error("Error loading players:", err);
        const list = document.getElementById("player_list");
        list.innerHTML = "<li>Could not load players</li>";
        return;
    }
    const chooseBtn = document.getElementById("choose_player_but");
    const newPlayerBtn = document.getElementById("new_player_but");

    // player selection button
    chooseBtn.addEventListener("click", () => {
        const selected = sessionStorage.getItem("selectedPlayer");
        if (!selected) {
            alert("Pick a player first!");
            return;
        }
        window.location.href = "../views/main_menu.html";
    });

    // create a new player
    newPlayerBtn.addEventListener("click", () => {
        window.location.href = "../views/new_player.html";
    });
});


function renderPlayerList(players) {
    const list = document.getElementById("player_list");
    list.innerHTML = "";
    players.forEach(p => {
        const row = document.createElement("li");
        row.textContent = p.name;
        row.addEventListener("click", () => {
            // clear previous highlight
            list.querySelectorAll("li").forEach(li => li.classList.remove("selected"));

            row.classList.add("selected");
            sessionStorage.setItem("selectedPlayer", p.name);

            const chooseBtn = document.getElementById("choose_player_but");
            chooseBtn.disabled = false;
        });

        list.appendChild(row);
    });
}
