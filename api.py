#!/home/asiegel/dev/bin/python

import sys
import math
import MySQLdb
import json
from PIL import Image
import StringIO
import cgi
import cgitb
cgitb.enable()

class SpatialMemory:

	def __init__(self):
		self.connectToDatabase()
		self.form = cgi.FieldStorage()
		action = cgi.escape(self.form["action"].value)
		if action == "local":
			self.listLocalPhotos()
		elif action == "photo":
			self.getPhoto()
		elif action == "info":
			self.getPhotoInfo()

	def connectToDatabase(self):
		self.conn = MySQLdb.connect(host="localhost", user="asiegel_web", passwd="buttslol!", db="asiegel_histmap")
		self.c = self.conn.cursor()

	def getPhoto(self):
		# return photo sized to constrain to user's screen dimensions
		id = cgi.escape(self.form["id"].value)
		sw = int(cgi.escape(self.form["sw"].value))
		sh = int(cgi.escape(self.form["sh"].value))
		self.c.execute("SELECT collection_id,item_id FROM photos WHERE id = "+id)
		result = self.c.fetchone()
		#print str(result[0]) +"/"+ str(result[1]) +".jpg"
		img = Image.open("photos/"+ str(result[0]) +"/"+ str(result[1]) +".jpg")
		neww = sw
		newh = (sw / float(img.size[0])) * img.size[1]
		img = img.resize((int(neww), int(newh)), Image.BICUBIC)
		output = StringIO.StringIO()
		img.save(output, "JPEG")
		sys.stdout.write("Content-Type: image/jpeg\r\n\r\n" + output.getvalue())
		output.close()

	def getPhotoInfo(self):
		# return line with photo information
		print "Content-Type: text/plain\n"
		id = cgi.escape(self.form["id"].value)
		self.c.execute("SELECT * FROM photos WHERE id = "+id)
		r = self.c.fetchone()
		jsonOutput = json.dumps({"id": r[0], "item_id": r[1], "page_id": r[2], "collection_id": r[3], "title": r[4], "lat": r[5], "lon": r[6], "circa": r[7]}, sort_keys=True)
		print jsonOutput

	def getDistanceInMeters(self, myLat, myLon, photoLat, photoLon):
		# calculate distance in meters between photo location and user location
		R = 6371000		# earths radius in meters
		myLatRads = math.radians(myLat)
		photoLatRads = math.radians(photoLat)
		latDiff = math.radians(photoLat - myLat)
		lonDiff = math.radians(photoLon - myLon)
		a = math.sin(latDiff/2) * math.sin(latDiff/2) + math.cos(myLatRads) * math.cos(photoLatRads) * math.sin(lonDiff/2) * math.sin(lonDiff/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		return R * c

	def listLocalPhotos(self):
		# list up to 20 archived photos within the radius
		# TODO: switch to haversine distance calculation
		print "Access-Control-Allow-Origin: *\n"
		#print "Content-Type: text/plain\n"
		myLat = cgi.escape(self.form["lat"].value)
		myLon = cgi.escape(self.form["lon"].value)
		radius = "0.005"
		self.c.execute("SELECT *, (SELECT sqrt(pow(lat - "+ myLat +", 2) + pow(lon - "+ myLon +", 2))) AS dist FROM photos WHERE abs(lat - "+ myLat +") < "+ radius +" AND abs(lon - "+ myLon +") < "+ radius +" ORDER BY dist ASC")
		#self.c.execute("SELECT DISTINCT item_id, (SELECT sqrt(pow(lat - "+ myLat +", 2) + pow(lon - "+ myLon +", 2))) AS dist FROM photos WHERE abs(lat - "+ myLat +") < "+ radius +" AND abs(lon - "+ myLon +") < "+ radius +" ORDER BY dist ASC")
		results = self.c.fetchmany(20)
		print "["
		count = 0
		for r in results:
			dist = self.getDistanceInMeters(float(myLat), float(myLon), float(r[5]), float(r[6]))
			jsonOutput = json.dumps({"id": r[0], "item_id": r[1], "page_id": r[2], "collection_id": r[3], "title": r[4], "lat": r[5], "lon": r[6], "circa": r[7], "dist": str(dist)}, sort_keys=True)
			#jsonOutput = json.dumps({"item_id": r[0], "dist": r[1]}, sort_keys=True)
			count += 1
			if count < len(results):
				print jsonOutput +","
			else:
				print jsonOutput
		print "]"

sm = SpatialMemory()
