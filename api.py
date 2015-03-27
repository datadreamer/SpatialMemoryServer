#!/home/asiegel/dev/bin/python

print "Content-Type: text/plain\n"

import MySQLdb
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
myLat = form["lat"].value
myLon = form["lon"].value
radius = "0.005"

conn = MySQLdb.connect(host="localhost", user="asiegel_web", passwd="buttslol!", db="asiegel_histmap")
c = conn.cursor()
c.execute("SELECT *, (SELECT sqrt(pow(lat - "+ myLat +", 2) + pow(lon - "+ myLon +", 2))) AS dist FROM photos WHERE abs(lat - "+ myLat +") < "+ radius +" AND abs(lon - "+ myLon +") < "+ radius +" ORDER BY dist ASC")

results = c.fetchmany(20)

for r in results:
	print(r)