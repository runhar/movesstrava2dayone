# coding: utf-8
# Moves and Strava Data to Day One


import requests, json, datetime, pprint, webbrowser, urllib, Image, clipboard, sys, polyline, keychain
from io import BytesIO
from stravalib.client import Client


class MovesStrava2Dayone():
	'''Purpose: retrieve data from Moves and Strava to generate markdown text and google map image for Day One app. '''
	def __init__(self):
		self.places = [] 
		self.points = [] 
		if len(sys.argv) > 1:
			nrdays = int(sys.argv[1])
		else:
			nrdays = int(raw_input('0 is today, 1 is yesterday etc.'))
		choosenDate = datetime.datetime.now() - datetime.timedelta(days=nrdays)
		moves = self.MovesHistory(choosenDate)
		strava, self.stravarunpaths = self.Strava(choosenDate)
		output = '**' + choosenDate.strftime('%d-%m-%Y') + ':**\n' + moves + strava		
		output = output.encode('utf-8')
		self.googlemap()
		url = 'dayone://post?entry=' + urllib.quote(output) + '&imageClipboard=1'
		msg=webbrowser.open(url)
		
	def Strava(self, choosenDate):
		'''Get data from Strava for given date. information about run is presented in markdown text. Google map polyline is saved to use in map if Moves did not record run'''
		strava_token = keychain.get_password('strava','api')
		client = Client(access_token=strava_token)
		strava_output = ''
		acts = client.get_activities(limit=10)
		runpaths = []
		for a in acts:
			if a.start_date.date() == choosenDate.date():
				strava_output += '\n\n**%s %s**\n' % (a.start_date_local.time(), a.name)
				strava_output += '%s km in %s (%s km/u)\n' % (round(float(a.distance)/1000, 1), a.elapsed_time, round(float(a.average_speed)*3.6,1))
				strava_output += 'Splits:\n'
				lapnr = 1
				for lap in a.laps:
					strava_output += '%s. %s\n' % (lapnr, lap.elapsed_time)	
					lapnr += 1
				try:
					runpaths.append(a.map.summary_polyline)
				except:
					pass
		return strava_output, runpaths
				
	
	def googlemap(self):
		url='http://maps.googleapis.com/maps/api/staticmap?sensor=false&maptype=roadmap'
		url = url + '&format=png&size=800x600&scale=1'
		group=''
		newpoints = []
		colorpath = {'walking': '0x00d55a','running' : '0x660f4', 'transport' : '0x848484', 'cycling' : '0x00cdec', '':''}
		run_in_moves = False
		for point in self.points:
			if point['group'] == 'running':
				run_in_moves = True
			if point['group'] == group:									newpoints.append((point['lat'],point['lon']))
			else:
				try:
					path = polyline.encode(newpoints)
					print path
				except:
					path = ''
				url = url + '&path=color:' + colorpath[group] + '%7Cweight:5%7Cenc:' + path				
				newpoints = [(point['lat'],point['lon'])]
				group = point['group']
		# do not forget final segment
		url = url + '&path=color:' + colorpath[group] + '%7Cweight:5%7Cenc:' + polyline.encode(newpoints)
		# add strava runs if run not recorded in Moves data
		if not run_in_moves:
			for run in self.stravarunpaths:
				url = url + '&path=color:' + colorpath['running'] + '%7Cweight:5%7Cenc:' + run
		url = url + '&markers=color:blue%7Csize:normal' + self.coordstostring(self.places)
		#print url
		img = Image.open(BytesIO(urllib.urlopen(url).read()))
		clipboard.set_image(img)
	
	def coordstostring(self,ar):
		locstr = ''
		for point in ar:
			locstr = locstr + '%7C' + point['lat'] + ',' + point['lon']
		return locstr
	
	def strtime(self,segment):
		startTimeTmp = str(segment['startTime'])
		startTimeTime = datetime.datetime.strptime(startTimeTmp[:15], '%Y%m%dT%H%M%S')
		endTimeTmp = str(segment['endTime'])
		endTimeTime = datetime.datetime.strptime(endTimeTmp[:15], '%Y%m%dT%H%M%S')
		startTime = startTimeTime.strftime('%H:%M')
		endTime = endTimeTime.strftime('%H:%M')
		time = startTime + ' - ' + endTime + ': '
		return time
	
	def translation(self,str):
		return {
			'car': ' Auto',
			'train': ' Trein',
			'walking': ' Wandelen',
			'running': ' Hardlopen',
			'cycling': ' Fietsen',
			'transport': ' Vervoer',
			'funicular': ' Kabelbaan',
			'boat' : ' Boot',
			'tram' : ' Tram',
			'bus' : ' Bus',
			'airplane' : ' Vliegtuig',
			'underground' : ' Metro'
		}[str]
	
	def MovesHistory(self,callDate):
		'''collects Moves data for given date. 
		Output consists of markdown text of activities and places and a summary. Also self.points is populated by (activity_type,lat,lon) and self.places by places (name, lat, lon). These are used for generating a map in self.googlemap'''
		access_token = keychain.get_password('moves','api')
		mytoken = '?access_token=' + access_token
		api_url = 'https://api.moves-app.com/api/1.1'
		output = ''
		with requests.Session() as s:
	
			iurl = 'https://api.moves-app.com/oauth/v1/tokeninfo' + mytoken
			i = s.get(iurl)
			status = i.json()
			print status
			callDateApi = callDate.strftime('%Y%m%d')
			lurl = api_url + '/user/storyline/daily/' + callDateApi + '?trackPoints=true&access_token=' + access_token
			l = s.get(lurl)
			storyline = json.loads(l.text)
			placesDict = storyline[0]
			segments = placesDict['segments']
			summary = placesDict['summary']
			output = ''
			for segment in segments:
				type = str(segment['type'])
				if type == 'move':
					activities = []
					for act in segment['activities']:
						activities.append(self.translation(str(act['activity'])))		
						group = act['group']					
						for trackpoint in act['trackPoints']:
							self.points.append({'group':group,'lat':trackpoint['lat'],'lon':trackpoint['lon']})
					sep = ','
					activities = sep.join(activities)
					output = output + '\n* ' + self.strtime(segment) + activities
				elif type == 'place':
					if str(segment['place']['type'])=='unknown':
						strname = 'Onbekende locatie'
					else:
						strname = segment['place']['name']
					self.places.append({'name':strname, 'lat':str(segment['place']['location']['lat']),'lon':str(segment['place']['location']['lon'])})	
					output = output + '\n* **' + self.strtime(segment) + ' [' + strname + '](https:maps.google.nl/?q=' + str(segment['place']['location']['lat']) + ',' + str(segment['place']['location']['lon']) + ')**'				
			# summary maken
			output = output + '\n\nSamenvatting\n'
			for activity in summary:
				output = output + '* ' + self.translation(str(activity['activity'])) + ': ' + str(int(round(int(activity['duration']/60)))) + ' minuten, ' + str(int(round(int(activity['distance']/1000)))) + ' km\n'	
		return output

if __name__ == "__main__":
	MovesStrava2Dayone()

