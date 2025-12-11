document.addEventListener("DOMContentLoaded", function () {
    const btnCreate = document.getElementById("create_player_btn");
    const inputName = document.getElementById("player_name_input");
    const msg = document.getElementById("status_message");

    // create player handler
    btnCreate.addEventListener("click", async () => {
        const raw = inputName.value.trim();

        // quick sanity check
        if (!raw) {
            msg.textContent = "Name cannot be empty.";
            return;
        }

        let res, payload;
        try {
            res = await fetch("http://127.0.0.1:5000/new_player", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: raw })
            });

            // could fail if backend crashes, wrap json in try
            try {
                payload = await res.json();
            } catch (jErr) {
                console.warn("json parse?", jErr);
                payload = {};
            }

            if (res.ok) {
                msg.textContent = "Player created!";
                // small delay just to show message
                setTimeout(() => {
                    location.href = "choose_player.html";
                }, 900);
            } else {
                msg.textContent = payload?.error || "Couldn't create player.";
            }
        } catch (netErr) {
            console.log("network?", netErr);
            msg.textContent = "Server seems down.";
        }
    });
});
