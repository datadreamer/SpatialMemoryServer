#!/home/asiegel/dev/bin/python

print "Content-Type: text/plain\n"

import MySQLdb
import json
import cgi
import cgitb
cgitb.enable()

class SpatialMemory:

	def __init__(self):
		self.connectToDatabase()
		self.listLocalPhotos()		

	def connectToDatabase(self):
		self.conn = MySQLdb.connect(host="localhost", user="asiegel_web", passwd="buttslol!", db="asiegel_histmap")
		self.c = self.conn.cursor()

	def listLocalPhotos(self):
		form = cgi.FieldStorage()
		myLat = form["lat"].value
		myLon = form["lon"].value
		radius = "0.005"
		self.c.execute("SELECT *, (SELECT sqrt(pow(lat - "+ myLat +", 2) + pow(lon - "+ myLon +", 2))) AS dist FROM photos WHERE abs(lat - "+ myLat +") < "+ radius +" AND abs(lon - "+ myLon +") < "+ radius +" ORDER BY dist ASC")
		results = self.c.fetchmany(20)
		print "["
		count = 0
		for r in results:
			jsonOutput = json.dumps({"id": r[0], "item_id": r[1], "page_id": r[2], "collection_id": r[3], "title": r[4], "lat": r[5], "lon": r[6], "circa": r[7], "dist": r[8]}, sort_keys=True)
			count += 1
			if count < len(results):
				print jsonOutput +","
			else:
				print jsonOutput
		print "]"

sm = SpatialMemory()