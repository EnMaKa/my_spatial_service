/**
 * Mapclick function that is listening if it is clicked and open popup which return the coords
 */
function onMapClick(e) {

    //alert("You clicked the map at " + e.latlng);

    // Do a reprojection to EPSG:3857 for DB query
    var projCoords = L.Projection.SphericalMercator.project(e.latlng);
    
    // Round Coords for backendcall 
    roundedCoordX = projCoords.x.toFixed(0);
    roundedCoordY = projCoords.y.toFixed(0);
    requestBuffer = 50;

    // TODO: make a a popup pin or something
    // GET-Request for information about the clicked location
    $.get('/geocode?lat='+roundedCoordX +'&lon='+roundedCoordY +'&buffer_size='+requestBuffer, function(geoResult){
        alert(geoResult);
    });

}

/**
 * Load map function creates a leaflet map with an osm-baselayer.
 */
function loadMap(){

    var myMap = L.map('mapid');
    myMap.setView([53.08, 8.80692], 13);

    var baseLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });

    baseLayer.addTo(myMap);

    myMap.on('click', onMapClick);
}

