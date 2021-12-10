
const auth_link = "https://www.strava.com/oauth/token?"

 function getActivities(res){

        const activities_link = `https://www.strava.com/api/v3/athlete/activities?access_token=${res.access_token}`
        fetch(activities_link)
            .then((res) => console.log(res.json()))
 }

 

function reAuthorize(){
    fetch(auth_link,{
        method: 'post',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        
        },

        body: JSON.stringify({

            client_id:'74829',
            client_secret: 'ef07d4ca8008e644d8c110559efda58d5fe8d05e',
            refresh_token: 'a786d604dafe3242852ecd44fd457f9a93628b42',
            grant_type: 'refresh_token'

        })

    }).then(res => res.json())
        .then(res => getActivities(res))

}

reAuthorize()