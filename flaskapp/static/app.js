let map;

function initMap() {

    fetch("/stations").then(response => {
        return response.json();


    }).then(data => {
        //console.log("data: ", data);

    map = new google.maps.Map(document.getElementById("map"), {
      center: { lat: 53.349804, lng: -6.260310},
      zoom: 13,
    });

    data.forEach(stations => {
        if(stations.available_bikes > 0){
            let cityCircleAvail = new google.maps.Circle({
              strokeColor: "#00CC00",
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: "#00CC00",
              fillOpacity: 0.35,
              map,
              center: { lat: stations.pos_lat, lng: stations.pos_lng },
              radius: 50,
        });}
        else {
            let cityCircleNotAvail = new google.maps.Circle({
              strokeColor: "#FF0000",
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: "#FF0000",
              fillOpacity: 0.35,
              map,
              center: { lat: stations.pos_lat, lng: stations.pos_lng },
              radius: 50,
            });}

        const marker = new google.maps.Marker({
            position: { lat: stations.pos_lat, lng: stations.pos_lng },
            map: map,


        });


        marker.addListener("click", () => {
            const infowindow = new google.maps.InfoWindow({

                content: '<h3>'+stations.name+'</h3><p> Available Stands: '+stations.available_bike_stands+
                '<br>Available Bikes: '+stations.available_bikes+'</p>' + "hellllloo",

            });
            infowindow.open(map,marker);
        });


    });

    }).catch(err => {
      console.log("OOPS!", err);
    });
}

//Weather
//SELECT ELEMENTS
const iconElement = document.querySelector(".weather-icon");
const tempElement = document.querySelector(".temperature-value p");
const descElement = document.querySelector(".temperature-description p");
const locationElement = document.querySelector(".location p");
//const notificationElement = document.querySelector(".notification");
//const windSpeedElement = document.querySelector(".notification");

//APP DATA
//const weather = {};
//weather.temperature = {
//   unit: "celsius"
//}


//Get weather from API
function getWeather(){

     fetch("/weather").then(response => {
         let weatherData = response.json();
         return weatherData;
     })
         .then(function(weatherData){
             let temperature = weatherData.temp;
             let description = weatherData.description;
             let iconId = weatherData.icon;
             let windSpeed = weatherData.wind_speed;
         })
         .then(function(){
             displayWeather();
             console.log(weatherData);
         })
}

//DISPLAY WEATHER TO UI
function displayWeather(){
    //iconElement.innerHTML = `<img src="icons/${weather.iconId}.png"/>`;
    //tempElement.innerHTML = `${weather.temperature.value}°<span>C</span>`;
    //descElement.innerHTML = weather.description;
    //locationElement.innerHTML = "Dublin";
    descElement.innerHTML = description;


}

