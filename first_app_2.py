from flask import Flask, render_template, url_for, redirect, flash
import RPi.GPIO as GPIO
from flask_sqlalchemy import SQLAlchemy
from drink_sort import drinks_sort
import json
import time
import pouring_2
import config
app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

with open("pump_config.json") as p:
	pumps = json.load(p)



drinks_sort()
pouring_2.pump_reset(pumps)

with open("poss_drinks.json") as d:
	drinks = json.load(d)

	
length = list(range(1,len(drinks)+1))

keys = list(drinks.keys())

config.serve = False

#home page and main carosel
@app.route('/')
def home_page():
	drinks_sort()
	with open("poss_drinks.json") as d:
		drinks = json.load(d)
	if GPIO.input(26) == False:
		flash("Bartender not in serving mode, flick switch to activate serving mode")
	length = list(range(1,len(drinks)))
	pouring_2.pump_reset(pumps)
	keys = list(drinks.keys())
	return render_template('carosel_6.html',drinks = drinks, slide_no = length, keys=keys)

@app.route('/busy')
def busy():
	return(render_template('busy.html'))

#drink > double up
@app.route('/<chosen_drink>')
def double_up(chosen_drink):
	if config.serve == True:
		return redirect('/busy')
	if GPIO.input(26) == False:
		return redirect('/')
	#config.serve = True  this was to try and avoid two poeple using at the same time
	return render_template('double_up.html',chosen_drink = chosen_drink)

#pouring of chosen drink
@app.route('/<chosen_drink>/<double>')
def pour_drink(chosen_drink,double):
	with open("poss_drinks.json") as d:
		drinks = json.load(d)
	with open("pump_config_3.json") as p:
		pumps = json.load(p)
	pouring_2.pump_reset(pumps)
	ing = dict(drinks[chosen_drink]['ing_pump'])
	pins = []
	double = str(double)
	pouring_2.pour(pumps,ing,double)	
	pouring_2.pump_reset(pumps)
	config.serve = False
	draw_ing = drinks[chosen_drink]["ing_draw"]
	if len(draw_ing) > 0:
		return render_template('draw.html', draw_ing = draw_ing,double = double,chosen_drink = chosen_drink)
	else:
		return render_template('pouring.html', drink = chosen_drink, drinks_list = drinks)

@app.route('/<chosen_drink>/<double>/draw')
def draw_test(chosen_drink, double):
	return render_template('pouring.html',drink = chosen_drink, drinks_list = drinks)

	
@app.route('/clear')
def clear_tubes():
	pouring_2.pump_clear(pumps)
	return render_template('clearing.html')



#manual pouring from pumps page
@app.route('/pour/<pump>')
def manual_pour(pump):
	with open("pump_config_3.json") as p:
		pumps = json.load(p)
	ing = pumps[pump]["value"]
	return render_template('manual_pour.html',pump = pump,ing = ing)

# Manual pouring and summery
@app.route('/pour/<pump>/active')
def active(pump):
	with open("pump_config_3.json") as p:
		pumps = json.load(p)
	mls_poured = pouring_2.man_pour(pumps,pump)
	msg = "You poured "+str(round(mls_poured,1))+"mls of "+str(pumps[pump]["value"])
	flash(msg)
	return redirect('/pumps')

#pumps pages
#main pump page
@app.route('/pumps')
def pump_layout():
	with open("pump_config_3.json") as p:
		pumps = json.load(p)
	return render_template('pumps_2.html', pumps = pumps)

#options of alt ingredients
@app.route('/pumps/<pump>')
def pump_change(pump):
	with open("pump_config_3.json") as p:
		pumps = json.load(p)
	all_ing = pouring_2.pump_set()
	return render_template('pumps_options.html', pumps = pumps, pump = pump, all_ing = all_ing)

#changing pump_config JSON to new arrangement
@app.route('/pumps/<pump>/<ing>')
def pump_change_2(pump, ing):
	with open("pump_config_3.json") as p:
		pumps = json.load(p)
	pumps[pump]['value'] = ing
	with open("pump_config_3.json","w") as p:
		json.dump(pumps,p,indent=4, sort_keys=True)
	return render_template("pumps_3.html", pump = pump, ing = ing)

#End screen of pump change sequence
@app.route('/pumps/<pump>/<ing>/<al>')
def pump_change_3(pump,ing,al):
	with open("pump_config_3.json") as p:
		pumps = json.load(p)
	pumps[pump]['al'] = str(al)
	with open("pump_config_3.json","w") as p:
		json.dump(pumps,p,indent=4, sort_keys=True)
	return render_template('pumps_4.html')

if __name__ == '__main__':
	app.secret_key = 'super secret key'
	app.run(debug=True, host='192.168.0.16')
