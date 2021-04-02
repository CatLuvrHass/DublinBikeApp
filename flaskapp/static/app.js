let map;

// const locationInfo = document.querySelector('#location-info');
//
// function getLocation(){
//     navigator.geolocation.getCurrentPosition(
//         (position) => {
//             const pos = {
//                 lat: position.coords.latitude,
//                 lng: position.coords.longitude,
//             };
//             document.getElementById("start").innerHTML = [pos.lat, pos.lng]
//             document.getElementById("end").innerHTML = [pos.lat, pos.lng]
//         });
//
// }

function initMap() {

    fetch("/stations").then(response => {
        return response.json();

    }).then(data => {
        // console.log("data: ", data);

    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 53.349804, lng: -6.260310},
      zoom: 14,
    });
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude,
            };
            var originDropDown = document.getElementById("start");
            var opt = document.createElement("option");

            opt.value= [pos.lat, pos.lng];
            opt.innerHTML = "mee";

            originDropDown.add(opt);
            console.log(pos.lng);
        });

    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    const onChangeHandler = function () {
    calculateAndDisplayRoute(directionsService, directionsRenderer);
    };
    document.getElementById("start").addEventListener("change", onChangeHandler);
    document.getElementById("end").addEventListener("change", onChangeHandler);
    citySelect();

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


function calculateAndDisplayRoute(directionsService, directionsRenderer) {
  directionsService.route(
    {
      origin: {
        query: document.getElementById("start").value,
      },
      destination: {
        query: document.getElementById("end").value,
      },
      travelMode: google.maps.TravelMode.BICYCLING,
    },
    (response, status) => {
      if (status === "OK") {
        directionsRenderer.setDirections(response);
      } else {
        window.alert("Directions request failed due to " + status);
      }
    }
  );
}

function citySelect(){

    const start_ele = document.getElementById('start');
    const end_ele = document.getElementById('end');
    fetch("/stations").then(result => {
        return result.json();
    }).then(another => {
        // console.log("anotherone: ", another);
            another.forEach(station =>{

                var originDropDown = document.getElementById("start");
                var opt = document.createElement("option");
                opt.value= [station.pos_lat,station.pos_lng];
                opt.innerHTML = station.name;

                originDropDown.add(opt);

                var originDropDown = document.getElementById("end");
                var opt = document.createElement("option");
                opt.value= [station.pos_lat,station.pos_lng];
                opt.innerHTML = station.name;

                originDropDown.add(opt);
    });
    });
}
