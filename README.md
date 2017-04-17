# movesstrava2dayone
Pythonista script for creating daily overview in Day One, using Google map, Moves and Strava

Little IOS Pythonista script to fetch data from Moves and Strava to create a daily overview
for the IOS DayOne app. For this to run you'll need a Moves and a Strava developer account.
Store the access tokens in keychain: keychain.set_password('moves', 'api','youraccesstoken').
Start the script in the Pythonista app, and enter the day you want to create an item for:
0 is today, 1 is yesterday etc.

The script will try to fetch data from your Moves and Strava account. It will create a list
of activities based on your Moves data. Then it will use the GPS data to create a Google map image
depicting where you've been that day, colored by type of activity.

Output example:

![Rome](Rome.jpeg?raw=true "Rome")

Date:		day month 2017 22:48:54 CEST
Weather:	9°C Mostly Sunny
Location:	Arco della Pace 6, Rome, Lazio, Italië


**dd-mm-2017:**

* **23:53 - 07:24:  [Home](https:maps.google.nl/?q=41.886206573,12.4715751321)**
* 07:24 - 09:03:  Running, Walking, Running
* **09:03 - 10:57:  [Home](https:maps.google.nl/?q=41.886206573,12.4715751321)**
* 10:57 - 11:40:  Walking
* **11:40 - 13:45:  [Domus Aurea](https:maps.google.nl/?q=41.8913888889,12.4952777778)**
* 13:45 - 14:02:  Walking
* **14:02 - 14:08:  [Unknown location](https:maps.google.nl/?q=41.89656,12.494993)**
* 14:08 - 14:40:  Walking
* **14:40 - 14:50:  [Unknown location](https:maps.google.nl/?q=41.892822,12.483605)**
* **15:06 - 15:29:  [Giselda](https:maps.google.nl/?q=41.8867378381,12.4719803179)**
* 15:29 - 15:33:  Walking
* **15:33 - 15:40:  [Unknown location](https:maps.google.nl/?q=41.889419,12.473994)**
* 15:40 - 15:47:  Walking
* **15:47 - 19:46:  [Home](https:maps.google.nl/?q=41.886206573,12.4715751321)**
* 19:46 - 19:52:  Walking
* **19:52 - 19:54:  [Unknown location](https:maps.google.nl/?q=41.890069,12.474236)**
* 19:54 - 20:33:  Walking
* **20:33 - 20:35:  [Unknown location](https:maps.google.nl/?q=41.901817,12.46647)**
* 20:35 - 20:45:  Walking
* 20:45 - 20:47:  Walking
* **20:47 - 21:26:  [Abbey Theatre Irish Pub Rome](https:maps.google.nl/?q=41.8982747704,12.4705430284)**
* 21:26 - 21:39:  Walking
* **21:39 - 21:42:  [Unknown location](https:maps.google.nl/?q=41.890465,12.474261)**
* 21:42 - 21:49:  Walking
* **21:49 - 06:35:  [Home](https:maps.google.nl/?q=41.886206573,12.4715751321)**

Summary
*  Walking: 236 minuten, 15 km
*  Running: 95 minuten, 16 km


**07:26:47 Morning run**
15.0 km in 1:36:54 (10.2 km/u)
Laps:
1. 0:06:59
2. 0:05:51
3. 0:05:59
4. 0:05:40
5. 0:06:18
6. 0:05:36
7. 0:06:30
8. 0:07:28
9. 0:07:25
10. 0:05:30
11. 0:05:20
12. 0:06:48
13. 0:07:35
14. 0:07:19
15. 0:05:09
16. 0:01:21



Why Strava? I often run without my iPhone, but with my sports watch.
When my run is not stored on Moves, I use the data from my sports watch which synchs with Strava.

Requires stravalib Python library.
