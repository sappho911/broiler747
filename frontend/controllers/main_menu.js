document.addEventListener("DOMContentLoaded", () => {
    const playerName = sessionStorage.getItem("selectedPlayer");
    const playerSlot = document.getElementById("player_name");
    const newGameBtn = document.getElementById("new_game_but");

    if (playerName) {
        playerSlot.textContent = `Player: ${playerName}`;
        newGameBtn.disabled = false;
    } else {
        playerSlot.textContent = "No player selected";
    }


});