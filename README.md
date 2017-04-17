# movesstrava2dayone
Pythonista script for creating daily overview in Day One, using Google map, Moves and Strava

Little IOS Pythonista script to pull data from Moves and Strava to create a daily overview
for the IOS DayOne diary app. For this to run you'll need a Moves and a Strava developer account.
Store the access tokens in keychain: keychain.set_password('moves', 'api','youraccesstoken').
Start the script in the Pythonista app, and enter the day you want to create an item for: 
0 is today, 1 is yesterday etc.

The script will try to fetch data from your Moves and Strava account. It will create a list
of activities based on your Moves data. Then it will use the GPS data to create a Google map image 
depicting where you've been that day, colored by type of activity.

![Alt text](Rome.jpeg?raw=true "Rome")

Why Strava? I often run without my iPhone, but with my sports watch.
When my run is not stored on Moves, I use the data from my sports watch which synchs with Strava.
