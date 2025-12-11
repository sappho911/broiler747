import { getPlayers } from "../model/players.js";


document.addEventListener("DOMContentLoaded", async () => {

    let list;   

    try {
        const allPlayers = await getPlayers();
        
        buildList(allPlayers);

        const chooseBtn = document.getElementById("choose_player_but");
        const newBtn = document.getElementById("new_player_but");

        chooseBtn.addEventListener("click", () => {
            const p = sessionStorage.getItem("selectedPlayer");
            if (p) {
                window.location.href = "../views/main_menu.html";
            } else {
                alert("Please select a player.");
            }
        });

        newBtn.addEventListener("click", () => {
            window.location.href = "../views/new_player.html";
        });

    } catch (e) {
        console.log("Could not load players:", e);
        const listElement = document.getElementById("player_list");
        listElement.innerHTML = "<li>Could not load players. Check console.</li>";
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


function buildList(players) {
    const container = document.getElementById("player_list");
    if (!container) return;  

    container.innerHTML = "";

    players.forEach((plr) => {

        const item = document.createElement("li");
        item.textContent = plr.name;

        item.onclick = () => {

            const all = document.querySelectorAll("#player_list li");
            for (let i = 0; i < all.length; i++) {
                all[i].classList.remove("selected");
            }

            item.classList.add("selected");
            sessionStorage.setItem("selectedPlayer", plr.name);

            const pickBtn = document.getElementById("choose_player_but");
            if (pickBtn) pickBtn.disabled = false;
        };

        container.appendChild(item);
    });
}
