let map;

function initMap() {

    fetch("/stations").then(response => {
        return response.json();


    }).then(data => {
        console.log("data: ", data);

    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 53.349804, lng: -6.260310},
      zoom: 14,
    });

    data.forEach(stations => {
        const marker = new google.maps.Marker({
            position: { lat: stations.pos_lat, lng: stations.pos_lng },
            map: map,

        });

        marker.addListener("click", () => {
            const infowindow = new google.maps.InfoWindow({

                content: '<h3>'+stations.name+'</h3><p> Available Stands: '+stations.available_bike_stands+
                '<br>Available Bikes: '+stations.available_bikes+'</p>',

            });
            infowindow.open(map,marker);
        });
    });

    }).catch(err => {
      console.log("OOPS!", err);
    });
}
