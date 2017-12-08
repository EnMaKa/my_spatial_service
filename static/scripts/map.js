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


    proj4.defs("EPSG:3857","+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs");
    proj4.defs('urn:x-ogc:def:crs:EPSG:4326', proj4.defs('EPSG:4326'));

    var dbProj = proj4.Proj('EPSG:3857');
    var mapProj = proj4.Proj('EPSG:4326');

    /**
     * Mapclick function that is listening if it is clicked and open popup which return the coords
     */
    function onMapClick(e) {

        console.log(e.latlng);
        
        // Do a reprojection to EPSG:3857 for DB query
        var projCoords = L.Projection.SphericalMercator.project(e.latlng);
        
        // Round Coords for backend call 
        var roundedCoordX = projCoords.x.toFixed(0);
        var roundedCoordY = projCoords.y.toFixed(0);
        var requestBuffer = 150;

        posInfo.setLatLng(e.latlng);
        
        // GET-Request for information about the clicked location
        $.get('/geocode?lat='+roundedCoordX +'&lon='+roundedCoordY +'&buffer_size='+requestBuffer, function(geoResult){
            posInfo.setContent("Position you've clicked at: "+ e.latlng.lat.toFixed(4) + "," + e.latlng.lng.toFixed(4)
                + "<br/>" + "Address(es): " + geoResult);
            posInfo.openOn(myMap);
        });

    }    

    // backend search call function on button click
    $('#searchbutton').click(function(){

        var searchBar =$('#searchbar');
        var searchBarVal = searchBar.val();
        
        // GET-Request 
        $.get('/locatestreet?address='+searchBarVal, function(result){
            
            //transform to map coords
            var resPoint= proj4.Point(result.lon.toFixed(4),result.lat.toFixed(4));
            var newCoords = proj4.transform(dbProj, mapProj,resPoint);
            var transPoint = L.latLng(newCoords.x.toFixed(4), newCoords.y.toFixed(4));
            console.log(transPoint);
            // pan to given coords
            myMap.panTo(transPoint);
            posInfo.setLatLng(transPoint);
            posInfo.setContent(result.adress);
            posInfo.openOn(myMap);
        });

        searchBar.empty();
    });

    myMap.on('click', onMapClick);
}








4