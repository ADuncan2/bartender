from flask import Flask, render_template, url_for
import RPi.GPIO as GPIO
from drink_sort import drinks_sort
import json
import time

GPIO.setmode(GPIO.BCM)



with open("pump_config.json") as p:
	pumps = json.load(p)



app = Flask(__name__)

drinks_sort()

with open("poss_drinks.json") as d:
	drinks = json.load(d)

	
length = list(range(1,len(drinks)+1))

keys = list(drinks.keys())

@app.route('/')
def home_page():
	for pump in pumps:
		pin = pumps[pump]['pin']
		GPIO.setup(pin , GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)
	return render_template('carosel_6.html',drinks = drinks, slide_no = length, keys=keys)

@app.route('/<chosen_drink>')
def pour_drink(chosen_drink):
	ing = drinks[chosen_drink]['ing_pump']
	pins = []
	for i in ing:
		for p in pumps:
			if pumps[p]['value'] == i:
				pins.append(pumps[p]['pin'])
				GPIO.output(pumps[p]['pin'], GPIO.HIGH)
			else:
				pass
	time.sleep(3)
	return render_template('pouring.html',drink = chosen_drink, drinks_list = drinks, pins = pins)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.16')
