import { getPlayers } from "../model/players.js";

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const players = await getPlayers();
        makePlayerList(players);
        const chooseBtn = document.getElementById("choose_player_but");
        const newPlayerBtn = document.getElementById("new_player_but");
        chooseBtn.addEventListener("click", () => {
            const selectedPlayer = sessionStorage.getItem("selectedPlayer");
            if (selectedPlayer) {
                window.location.href = "../views/main_menu.html";
            } else {
                alert("Please select a player first!");
            }
        });
        newPlayerBtn.addEventListener("click", () => {
            window.location.href = "../views/new_player.html";
        });

    } catch (error) {
        console.error("Failed to load players:", error);
        const playerList = document.getElementById("player_list");
        playerList.innerHTML = "<li>Failed to load players. Check console.</li>";
    }
});

function makePlayerList(players) {
    const playerList = document.getElementById("player_list");
    playerList.innerHTML = "";
    players.forEach(player => {
        const li = document.createElement("li");
        li.textContent = player.name;
        li.addEventListener("click", () => {
            // Deselect all
            document.querySelectorAll("#player_list li").forEach(item => {
                item.classList.remove("selected");
            });
            li.classList.add("selected");
            sessionStorage.setItem("selectedPlayer", player.name);
            document.getElementById("choose_player_but").disabled = false;
        });
        playerList.appendChild(li);
    });
}