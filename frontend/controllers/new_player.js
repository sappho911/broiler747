
document.addEventListener("DOMContentLoaded", () => {
    const createBtn = document.getElementById("create_player_btn");
    const nameInput = document.getElementById("player_name_input");
    const statusMessage = document.getElementById("status_message");

    createBtn.addEventListener("click", async () => {
        const name = nameInput.value.trim();
        if (name.length === 0) {
            statusMessage.textContent = "Name cannot be empty!";
            return;
        }
        try {
            const response = await fetch("http://127.0.0.1:5000/new_player", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name })
            });
            const result = await response.json();
            if (response.ok) {
                statusMessage.textContent = "Player created!";
                setTimeout(() => {
                    window.location.href = "choose_player.html";
                }, 1000);
            } else {
                statusMessage.textContent = result.error || "Error creating player.";
            }
        } catch (err) {
            console.error(err);
            statusMessage.textContent = "Server error.";
        }
    });
});