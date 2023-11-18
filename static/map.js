var map = L.map('map').setView(destination, 14);

L.tileLayer('https://tile.openstreetmap.de/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

L.Routing.control({
    waypoints: [
        L.latLng(50.6985155,10.9234212),
        L.latLng(50.6829, 10.9377)
    ]
}).addTo(map);
