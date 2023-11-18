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
        calculateRoute();
    }
    setTimeout(trackLocation, 5000); // alt.: setInterval()
}
map.on('locationfound', onLocationFound);
map.locate({setView: true});

// Routing with Graphhopper
// 11/18/2013: Free version has 15,000 requests per day
function calculateRoute() {
    if (!user_location) return; // Break if locating failed
    console.log("Routing...");
    L.Routing.control({
        waypoints: [
            L.latLng(user_location[0], user_location[1]),
            L.latLng(destination[0], destination[1])
        ],
        router: L.Routing.graphHopper(apikey, {
            urlParameters: {vehicle: 'car'}
        }),
        autoRoute: false, // To prevent excessive use of ressources
        createMarker: function() { // Only show destination marker
            L.marker(destination).addTo(map);
            return null;
        },
    }).addTo(map).route();
}
