g_author__ = 'Atul'

#Name Atul Konaje (Atul.Konaje@mavs.uta.edu)
#UTA ID 1001145198
#Course CSE6331 (2155-CSE-6331-004-ADV-TOPICS-IN-DATABASE-SYSTEMS--2015-Summer)
# import the Bottle framework
from bottle import static_file
from bottle import route, template, request,run
from urllib2  import urlopen
import json
import csv
import json
#http://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php
#Handle the inital request
@route('/',method="GET")
def welcome():

    output = static_file('default.html',root="views/")
    return output

def parse_process_csv(fileopen):
	reader = csv.reader(fileopen)
	line=reader.next()
	fieldnames=line
	print fieldnames
	data_dict = csv.DictReader(fileopen,fieldnames)
	final_value=[]
	#final_value.append(['Lat', 'Long', 'Name','mag'])
	i=0
	for row in data_dict:
		i=i+1
		if(row['latitude']=="FALSE" or row['longitude']=="FALSE" or row['mag']==""):
			continue
	#print(row['latitude'],row['longitude'])
		try:
			final_value.append([float(row['latitude']),float(row['longitude']),"Place:"+row['place']+"  Time: "+row['time'],float(row['mag'])])
		except ValueError:
			print(row['latitude'],row['longitude'],row['mag'])
	return final_value
		
#	if i==10:
#		break
#	print final_value   
	
#To recieve the csv file dropped
@route('/csvdata',method="POST")
def send():
	fileopen=request.files['file'].file
	#fname=request.files['file'].filename
	final_value=parse_process_csv(fileopen)
	print(type(final_value))
	#print(final_value)
	print(type(json.dumps(final_value)))
	return json.dumps(final_value)


@route('/getData/<duration>',method="GET")
def process(duration):
	url='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv'
	inpfile=urlopen(url);
	#inpfile=open("all_month.csv",'rb')
	final_value=parse_process_csv(inpfile)
	#print(final_value)
	return json.dumps(final_value)
	

@route('/geochart',"POST")	
def processrequest():
    print "proccessing"

run(host='0.0.0.0', port=3000, debug=True)
