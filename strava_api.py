import requests
import urllib3
import json

################################## CONNECT TO STRAVA  ##############################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "74829",
    'client_secret': 'ef07d4ca8008e644d8c110559efda58d5fe8d05e',
    'refresh_token': 'a786d604dafe3242852ecd44fd457f9a93628b42',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

################################## RETRIEVE DATA FROM STRAVA  ##############################################

#maybe the code should look through past activities until its find last known recorded id

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print('Activity Name:', my_dataset[0]["name"])
#print('Distance Traveled in Meters:', my_dataset[0]["distance"])
print('Unique activity id:', my_dataset[0]["id"])
new_distance = round(my_dataset[0]["distance"]/1000, 1)
activity_id = my_dataset[0]["id"]
print(new_distance, 'Km travelled')
print('\n')

new_data = 0

with open('JSON/strava_data.json') as json_file:
    current_distance = json.load(json_file)
    print(round(current_distance['distance'],1), 'Km distance so far')


last_activity_id = current_distance['activity_id']
#print(last_activity_id)
new_distance = round(float(current_distance['distance']) + float(new_distance),1)
print(new_distance, 'Km is the new total ditance')
print('\n')

   
################################## CHECK WHICH ZONE  ##############################################
print('\n')
    
zone = 0

#ditance range for each zone
zones = {1:[0,4], 2:[4,8], 3:[8,12], 4:[12,16], 5:[16,20], 6:[20,24], 7:[24,28]}

for x in range(7):
    i = x+1
    is_between = int(new_distance) in range(zones[i][0],zones[i][1])
    if is_between == True:
        print('you are now in zone:', i)
        zone = x

zone_update = zone + 1
print(zone_update)

with open('JSON/locations.json') as json_file:
    json_string = json.load(json_file)
    latitude = json_string[zone]['latitude']
    longitude = json_string[zone]['longitude']

################################## CHECK ACTIVITY TYPE  ##############################################

activity_name = my_dataset[0]["name"]

valid_text = ["Run", "commute", "Commute", "COMMUTE"]
email_contains_service = any(name in activity_name for name in valid_text)

print(email_contains_service)

################################## CHECK IF ITS A NEW ACTIVITY  ##############################################

if activity_id != last_activity_id:
    distance_record = {'distance': new_distance, 'activity_id': activity_id, 'zone': zone_update, 'latitude': latitude, 'longitude': longitude }
    
    print('New activity to record')
    json_strava_data = json.dumps(distance_record, indent = 2)
    with open('JSON/strava_data.json', 'w') as f:
        f.write(json_strava_data)
    
else:
    print('not a new activity')
    

