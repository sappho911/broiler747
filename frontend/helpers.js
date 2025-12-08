export const getData = async function (url, uploadData = undefined) {
  try {
    const fetchPromise = uploadData
      ? fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(uploadData),
        })
      : fetch(url);

    const res = await fetchPromise;
    const data = await res.json();

    if (!res.ok) throw new Error(`${data.message} (${res.status})`);

    return data;
  } catch (error) {
    throw error;
  }
};

// flyging animation

const map = L.map("map").setView([51.505, -0.09], 18);

L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
}).addTo(map);

const start = L.latLng(51.505, -0.09);
const end = L.latLng(61.2, 27.5);

const planeIcon = L.divIcon({
  html: "✈️",
  className: "plane-emoji",
  iconSize: [50, 50],
  iconAnchor: [16, 16],
});

const plane = L.marker(start, { icon: planeIcon }).addTo(map);

function fly(plane, start, end, duration = 10000) {
  const startTime = performance.now();

  function animate(time) {
    const progress = Math.min((time - startTime) / duration, 1);

    const lat = start.lat + (end.lat - start.lat) * progress;
    const lng = start.lng + (end.lng - start.lng) * progress;

    const pos = L.latLng(lat, lng);
    plane.setLatLng(pos);

    console.log(pos);

    map.setView(pos, 10, {
      animate: true,
      pan: {
        duration: 1,
      },
    });

    if (progress < 1) {
      requestAnimationFrame(animate);
    }
  }

  requestAnimationFrame(animate);
}

fly(plane, start, end, 100000);
