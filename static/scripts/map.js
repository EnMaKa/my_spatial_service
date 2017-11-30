/**
 * Load map function creates a leaflet map with an osm-baselayer.
 */
function loadMapAndFunctions(){

    var myMap = L.map('mapid');
    myMap.setView([53.08, 8.80692], 13);

    var baseLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });

    baseLayer.addTo(myMap);

    var posInfo = L.popup();    

    /**
     * Mapclick function that is listening if it is clicked and open popup which return the coords
     */
    function onMapClick(e) {
        
        // Do a reprojection to EPSG:3857 for DB query
        var projCoords = L.Projection.SphericalMercator.project(e.latlng);
        
        // Round Coords for backend call 
        var roundedCoordX = projCoords.x.toFixed(0);
        var roundedCoordY = projCoords.y.toFixed(0);
        var requestBuffer = 100;

        posInfo.setLatLng(e.latlng);
        
        // GET-Request for information about the clicked location
        $.get('/geocode?lat='+roundedCoordX +'&lon='+roundedCoordY +'&buffer_size='+requestBuffer, function(geoResult){
            posInfo.setContent("Position you've clicked at: "+ e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4)
                + "<br/>" + "Address(es) are: " + geoResult);
            posInfo.openOn(myMap);
        });

    }    

    // backend search call function on button click
    $('#searchbutton').click(function(){

        var searchBar =$('#searchbar');
        var searchBarVal = searchBar.val();
        
        // GET-Request 
        $.get('/locatestreet?address='+searchBarVal, function(result){
            alert(result);
        });

        searchBar.empty();
    });

    myMap.on('click', onMapClick);
}








