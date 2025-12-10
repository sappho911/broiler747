document.addEventListener("DOMContentLoaded", () => {
    loadStatistics();
});

async function loadStatistics() {
    const tableBody = document.querySelector("#statistics_table tbody");
    const title = document.getElementById("statistics_title");
    try {
        const response = await fetch("http://127.0.0.1:5000/api/players/stats");
        const stats = await response.json();
        if (!stats || stats.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" style="color:#ff9999; font-size:22px;">
                        No statistics available yet.
                    </td>
                </tr>`;
            return;
        }
        tableBody.innerHTML = "";
        stats.forEach(player => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${player.name}</td>
                <td>${player.easy_score}</td>
                <td>${player.medium_score}</td>
                <td>${player.hard_score}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error loading stats:", error);
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" style="color:red; font-size:22px;">
                    Failed to load statistics
                </td>
            </tr>`;
    }
}