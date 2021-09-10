# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 18:59:19 2020

@author: adunc
"""
import json

def drinks_sort():
    with open('drinks_bible_2.json') as f:
      data = json.load(f)
    
    with open('pump_config_3.json') as p:
        pumps = json.load(p)
    
    with open('draw_config.json') as d:
        draws = json.load(d)
    
    pump_list = []
    draw_list = []
    poss_drinks = {}
    
    for i in pumps:
        pump_list.append(pumps[i]["value"])

    for i in draws:
        draw_list.append(draws[i]["value"])
    
    for i in data:
        d = data[i]["ing_pump"]
        draw = data[i]["ing_draw"]
        count = 0
        ing_p = list(d)
        ing_d = list(draw)
        ing = ing_p + ing_d
        l = len(ing_p) + len(ing_d)
        for d in ing:
            dr = str(d)
            if dr in pump_list:
                count= count + 1
            if dr in draw_list:
                count = count + 1
            else:
                pass
        if l == count:
            poss_drinks[i] = data[i]
            with open('poss_drinks.json', 'w') as json_file:
                json.dump(poss_drinks, json_file, indent=4, sort_keys=True)
        else:
            pass    
