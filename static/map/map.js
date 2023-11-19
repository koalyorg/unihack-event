// Initialize map
var j = i;
var map = [];
map[j] = L.map('map' + j).setView(destination[j], 14);
L.tileLayer('https://tile.openstreetmap.de/{z}/{x}/{y}.png', {
	maxZoom: 18,
	attribution: '&copy; <a href="openstreetmap.org/copyright">OpenStreetMap</a> contributors | <a href="www.graphhopper.com">GraphHopper</a> | <a href="nominatim.org">Nomatim</a>'
}).addTo(map[j]);
L.marker(destination[j]).addTo(map[j]);

// Track User
var user_location = undefined;
var first_tracking = true;
function trackLocation() {
    map[j].locate();
}
function onLocationFound(e) {
    L.circleMarker(e.latlng, 10).addTo(map[j]);
    user_location = [e.latitude, e.longitude];
    if (first_tracking) {
        first_tracking = false;
        calculateRoute(); // alt.: setInterval(...)
    }
    setTimeout(trackLocation, 5000);
}
function onLocationError(e) {
    console.log("Error" + e.message);
    setTimeout(trackLocation, 2000)
}
map[j].on('locationfound', onLocationFound);
if (!disable_routing) { map[j].locate({setView: true}); }

// Routing with Graphhopper
// 11/18/2013: Free version has 15,000 requests per day
function calculateRoute() {
    if (!user_location) return;
    if (!apikey) return;
    L.Routing.control({
        waypoints: [
            L.latLng(user_location[0], user_location[1]),
            L.latLng(destination[j][0], destination[j][1])
        ],
        router: L.Routing.graphHopper(apikey, { urlParameters: {vehicle: 'foot'} }),
        autoRoute: false, // To prevent excessive use of ressources
        createMarker: function() { return null; }, // Removes default markers
        lineOptions: { styles: [{color: 'red', weight: 5}] },
    }).addTo(map[j]).route();
}
