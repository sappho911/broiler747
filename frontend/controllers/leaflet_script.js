document.addEventListener("DOMContentLoaded", async () => {

    // try to read the route info stored on the previous page
    const game = JSON.parse(sessionStorage.getItem("currentGame")) || {};

    const startCode = game.startAirport;
    const endCode = game.endAirport;

    // if something is missing, show default view (still prevents crash)
    if (!startCode || !endCode) {
        console.warn("Missing route data. Using defaults.");
    }

    // We need airport coordinates → load airports again (lightweight)
    let airports = [];
    try {
        const res = await fetch("http://127.0.0.1:5000/airports");
        const json = await res.json();
        airports = json.airports || [];
    } catch (err) {
        console.error("Could not load airports:", err);
        airports = [];
    }

    function findAirport(code) {
        return airports.find(ap =>
            ap.iata_code === code ||
            ap.ident === code
        );
    }

    const startA = findAirport(startCode);
    const endA = findAirport(endCode);

    // default fallback if coordinates missing
    const startLat = startA?.latitude || 51.505;
    const startLon = startA?.longitude || -0.09;
    const endLat   = endA?.latitude || 61.2;
    const endLon   = endA?.longitude || 27.5;

    // init Leaflet
    const map = L.map("minimap").setView([startLat, startLon], 8);

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18
    }).addTo(map);

    const planeIcon = L.divIcon({
        html: "✈️",
        className: "plane-emoji",
        iconSize: [40, 40],
        iconAnchor: [20, 20],
    });

    const startPos = L.latLng(startLat, startLon);
    const endPos = L.latLng(endLat, endLon);

    const plane = L.marker(startPos, { icon: planeIcon }).addTo(map);

    // simple human-style animation
    function flyPlane() {
        const duration = 15000; // 15s
        const t0 = performance.now();

        function frame(t) {
            const p = Math.min((t - t0) / duration, 1);

            const lat = startPos.lat + (endPos.lat - startPos.lat) * p;
            const lng = startPos.lng + (endPos.lng - startPos.lng) * p;

            const pos = L.latLng(lat, lng);
            plane.setLatLng(pos);

            map.setView(pos, 8, { animate: true });

            if (p < 1) requestAnimationFrame(frame);
        }

        requestAnimationFrame(frame);
    }

    flyPlane();
});