import os
import re
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/<string:dateString>')
def giveJSON(dateString):
	#Find out if string contains letters or digits only
	regex = '[a-zA-Z]'
	m = re.match(regex, dateString)
	
	natural = ""
	timestamp = ""
	
	#Natural Date
	if m:
		return "Natural Date"
	#Unix Timestamp
	else:
		timestamp = dateString
		dateObj = date.fromtimestamp(float(dateString))
		natural = naturalDateString(dateObj.year, dateObj.month, dateObj.day)
	
	object = {'unix' : timestamp,'natural' : natural,}
		
	return jsonify(object)
		
def naturalDateString(year,month,day):
	months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	dateString = str.format("{0} {1}, {2}",months[month-1], str(day), str(year))
	return dateString
		
if __name__ == '__main__':
	app.secret_key = "super-secret-key"
	app.debug = True
	app.run(host = os.environ.get('IP', '0.0.0.0'), port = int(os.environ.get('PORT', 8080)))