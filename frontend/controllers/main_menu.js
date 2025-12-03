import { return_main_menu } from "../controllers/choose_player.js";

async function check_player_selection(){
    const playerChosen = return_main_menu();
    return playerChosen;
}
document.addEventListener("DOMContentLoaded", () => {
    check_player_selection();
});