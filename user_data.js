fetch("./JSON/strava_data.json")
.then(response => {
   return response.json();
})
.then(data => console.log(data));



fetch("./JSON/locations.json")
.then(response => {
   return response.json();
})
.then(data => console.log(data));