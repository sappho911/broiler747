document.addEventListener("DOMContentLoaded", () => {
    const playerName = localStorage.getItem("selectedPlayer");
    const playerSlot = document.getElementById("player_name");

    if (playerName) {
        playerSlot.textContent = `Player: ${playerName}`;
    } else {
        playerSlot.textContent = "No player selected";
    }
});