import { getPlayers } from "../model/players.js";
// Initialize the player list on page load:
document.addEventListener("DOMContentLoaded", async () => {
    const players = await getPlayers();
    makePlayerList(players);
});
// Create the player list in the DOM and add selected one to LocalStorage to :
function makePlayerList(players){
    const playerList = document.getElementById("player_list");
    //some player_name is selected for default, user then chooses a player name and buttons is enabled
    players.forEach(player => {
        const li = document.createElement("li");
        li.textContent = player.name;
        li.addEventListener("click", () => {
            // remove previous selection
            document.querySelectorAll("#player_list li").forEach(item =>
                item.classList.remove("selected")
            );
            // add selection to clicked one
            li.classList.add("selected");
            document.getElementById("choose_player_but").disabled = false;
            // store selected player globally
            localStorage.setItem("selectedPlayer", player.name);
        });
        playerList.appendChild(li);
    });
}

export function return_main_menu(){
    if (playerChosen()){
         let chooseButton = document.getElementById("choose_player_but");
         chooseButton.disabled = false;
    }
    else{
        let chooseButton = document.getElementById("choose_player_but");
        chooseButton.disabled = true;
    }
}