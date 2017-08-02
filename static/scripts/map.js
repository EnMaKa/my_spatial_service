function loadMap(){

    var myMap = L.map('mapid');
    myMap.setView([53.08, 8.80692], 13);

    var baseLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });

    baseLayer.addTo(myMap);

	function onMapClick(e) {
	
    	alert("You clicked the map at " + e.latlng);

    	//do a projection to EPSG:3857
		var projCoords = L.Projection.SphericalMercator.project(e.latlng);
		console.log(projCoords.x);
		console.log(projCoords.y);
	}
    
    myMap.on('click', onMapClick);
}

