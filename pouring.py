import time
import RPi.GPIO as GPIO
import json

def pour(pumps,ings):
	multi = 1
	flow_rate = 0.17 
	but = False
	for p in pumps:
		for i in ings:
			if GPIO.input(26) == True:
				if i == pumps[p]["value"]:
					if pumps[p]["al"] == "y":
						t_on = ings[i]*flow_rate*multi
						pin = pumps[p]["pin"]
						GPIO.output(pin, True)
						time.sleep(t_on)
						GPIO.output(pin,False)
					else:
						t_on = ings[i]*flow_rate*multi
						pin = pumps[p]["pin"]
						GPIO.output(pin, True)
						time.sleep(t_on)
						GPIO.output(pin,False)
							
def pump_clear(pumps):
	for pump in pumps:
		pin = pumps[pump]['pin']
		GPIO.setup(pin , GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(4)
		GPIO.output(pin, GPIO.LOW)	
			
def man_pour(pumps,pump):
	pin = pumps[pump]["pin"]
	GPIO.setup(pin , GPIO.OUT)
	state = False
	pouring = True
	flow_rate = 0.17
	mls_poured = 0
	t0 = time.time() + 10
	while pouring ==True: 
		t1=time.time()
		if GPIO.input(26) == True and state==False:
			GPIO.output(pin, GPIO.HIGH)
			state = True
			t2=time.time()
		elif GPIO.input(26) == False and state == True:
			GPIO.output(pin, GPIO.LOW)
			t0 = time.time()
			state = False
			mls_poured = mls_poured+((t0-t2)/flow_rate)
		elif GPIO.input(26) == False and state==False and t1-t0 > 5:
			pouring = False
			break
		time.sleep(0.1)
	return mls_poured
	
	 
def pump_reset(pumps):
	for pump in pumps:
		pin = pumps[pump]['pin']
		GPIO.setup(pin , GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)

def but_check(but):
	if GPIO.input(26) == True:
		but = True
	else:
		but = False

def pump_set():
	current_pumps = []
	with open('drinks_bible_2.json') as d:
		poss_dr = json.load(d)
	with open('pump_config.json') as p:
		pumps = json.load(p) 
		
	for pump in pumps:
		current_pumps.append(pumps[pump]['value'])
	all_ing = []
	for i in poss_dr:
		ing = poss_dr[i]["ing_pump"]
		for n in ing:
			if n in all_ing:
				pass
			else:
				all_ing.append(n)
	for j in all_ing:
		if j in current_pumps:
			all_ing.remove(j)
		else:
			pass
	all_ing.sort()
	return all_ing
