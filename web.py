import os
import re
import math
import string
import calendar
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/<string:dateString>')
def giveJSON(dateString):
	#Find out if string contains letters or digits only
	regex = '[\D+]'
	m = re.match(regex, dateString)
	
	natural = None
	timestamp = None
	
	
	
	#Natural Date
	if m:
		dateObj = isValidNaturalDate(dateString)
		if dateObj:
			timestamp = calendar.timegm(dateObj.timetuple())
			natural = dateString
		else:
			natural = None
			timestamp = None
	#Unix Timestamp
	else:
		regex = "\s+"
		match = re.search(regex,dateString)
		if match or (int(dateString) > math.pow(2,32)):
			natural = None
			timestamp = None
		else:
			timestamp = dateString
			dateObj = date.fromtimestamp(float(dateString))
			natural = naturalDateString(dateObj.year, dateObj.month, dateObj.day)
	
	object = {'unix' : timestamp,'natural' : natural,}
		
	return jsonify(object)
		
#Constructs a natural date string of the form "MONTH DAY, YEAR" from indexes and integers
def naturalDateString(year,month,day):
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	dateString = str.format("{0} {1}, {2}",months[month-1], str(day), str(year))
	return dateString
	
#Checks to see if a date string is of the format "MONTH DAY, YEAR" and if that date is valid
#If so, returns a date object, else returns false
def isValidNaturalDate(dateString):
	months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
	days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	
	regex = "[A-Za-z]{1,10}\s\d{1,2},\s\d{4}"
	match = re.search(regex,dateString)
	if match:
		month = re.search("[A-Za-z]{1,10}",dateString).group(0)
		monthIndex = -1
		try:
			monthIndex = months.index(string.upper(month))+1
		except:
			return False
		
		day = re.search("\d{1,2}",dateString).group(0)
		
		year = re.search("\d{4}",dateString).group(0)
		
		try:
			return date(int(year), monthIndex,int(day))
		except:
			return False
		
	else:
		return False
		
if __name__ == '__main__':
	app.secret_key = "super-secret-key"
	app.debug = True
	app.run(host = os.environ.get('IP', '0.0.0.0'), port = int(os.environ.get('PORT', 8080)))