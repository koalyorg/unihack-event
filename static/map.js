// Initialize map
var map = L.map('map').setView(destination, 14);
L.tileLayer('https://tile.openstreetmap.de/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Track User
var user_location = undefined;
var first_tracking = true;
function trackLocation() {
    map.locate();
}
console.log(map);
function onLocationFound(e) {
    console.log("Location found")
    L.circleMarker(e.latlng, 10).addTo(map);
    user_location = [e.latitude, e.longitude];
    if (first_tracking) {
        first_tracking = false;
        calculateRoute(); // Not suitable for production (rate-limit, only car routes)
    }
    setTimeout(trackLocation, 5000);
}
map.on('locationfound', onLocationFound);
map.locate({setView: true});

// Routing
function calculateRoute() {
    if (!user_location) return; // Break if locating failed
    console.log("Routing...");
    L.Routing.control({
        waypoints: [
            L.latLng(user_location[0], user_location[1]),
            L.latLng(destination[0], destination[1])
        ],
        routeWhileDragging: true,
        // geocoder: L.Control.Geocoder.nominatim(),
        createMarker: function() { // Only show destination marker
            L.marker(destination).addTo(map);
            return null;
        }
    }).addTo(map);
    //setTimeout(trackLocation, 10000); // (!) This routing server is strictly rate-limited.
}
