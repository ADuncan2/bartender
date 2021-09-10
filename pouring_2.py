import time
import RPi.GPIO as GPIO
import json
import config
	
def pour(pumps,ings,double):
	flow_rate = 0.16#0.17
	cor_factor = 0.001
	if double == "y":
		multi = 2
	else:
		multi = 1
	but = False
	for p in pumps:
		for i in ings:
			if GPIO.input(26) == True:
				if i == pumps[p]["value"]:
					t_last_on = pumps[p]["last_on"]			#correcting for pipes emptying when not used for a while
					delta_t = time.time() - t_last_on
					if delta_t < 600: 						
						t_extra = delta_t*cor_factor
					else:
						t_extra = 2
					if pumps[p]["al"] == "y":			#distinguishing between alcoholic and non drinks for doubles
						t_on = ings[i]*flow_rate*multi + t_extra
						pin = pumps[p]["pin"]
						t_run = t_on + time.time()
						while time.time()< t_run:
							if GPIO.input(26) == True:
								GPIO.output(pin, True) #set to false for testing
							else:
								GPIO.output(pin,False)
						GPIO.output(pin,False)
						pumps[p]["last_on"] = round(time.time(),0) # record of when this pump was last used
					else:
						t_on = ings[i]*flow_rate*multi + t_extra
						pin = pumps[p]["pin"]
						test = time.time() - config.t_last_on[pin]
						t_run = t_on + time.time()
						while time.time()< t_run:
							if GPIO.input(26) == True:
								GPIO.output(pin, True) #set to false for testing
							else:
								GPIO.output(pin,False)
						GPIO.output(pin,False)
						pumps[p]["last_on"] = round(time.time(),0)
	with open("pump_config_3.json","w") as p:
		json.dump(pumps,p,indent=4, sort_keys=True)

def pump_clear(pumps):
	for pump in pumps:
		pin = pumps[pump]['pin']
		GPIO.setup(pin , GPIO.OUT)
		GPIO.output(pin, GPIO.HIGH)
		time.sleep(7)
		GPIO.output(pin, GPIO.LOW)
	
			
def man_pour(pumps,pump):
	pin = pumps[pump]["pin"]
	GPIO.setup(pin , GPIO.OUT)
	state = False
	pouring = True
	but = False
	flow_rate = 0.16
	cor_factor = 0.001
	mls_poured = 0
	t0 = time.time() + 10
	delta_t = time.time() - pumps[pump]["last_on"]
	if delta_t < 600: 						
		t_extra = delta_t*cor_factor
	else:
		t_extra = 2
	while pouring ==True:
		but = but_check() 
		t1=time.time()
		if but == True and state==False:
			GPIO.output(pin, GPIO.HIGH)
			state = True
			t2=time.time()
		elif but == False and state == True:
			GPIO.output(pin, GPIO.LOW)
			t0 = time.time()
			state = False
			mls_poured = mls_poured+((t0-t2-t_extra)/flow_rate)
			pumps[pump]["last_on"] = round(time.time(),0)
		elif but == False and state==False and t1-t0 > 5:
			pouring = False
			break
		time.sleep(0.1)
	with open("pump_config_3.json","w") as p:
		json.dump(pumps,p,indent=4, sort_keys=True)
	return mls_poured
	
	 
def pump_reset(pumps):
	for pump in pumps:
		pin = pumps[pump]['pin']
		GPIO.setup(pin , GPIO.OUT)
		GPIO.output(pin, GPIO.LOW)

def but_check():
	if GPIO.input(26) == True:
		but = True
	else:
		but = False
	return but

def pump_set():
	current_pumps = []
	with open('drinks_bible_2.json') as d:
		poss_dr = json.load(d)
	with open('pump_config_3.json') as p:
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
	print(current_pumps)
	current_pumps.sort()
	for j in current_pumps:
		if j in all_ing:
			all_ing.remove(j)
		else:
			pass
	all_ing.sort()
	print(all_ing)
	return all_ing
