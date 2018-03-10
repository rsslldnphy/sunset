#!/usr/bin/env python

import dotenv, json, os, requests, time

dotenv.load_dotenv('.env')

hue_ip    = os.getenv('HUE_IP')
hue_user  = os.getenv('HUE_USER')
hue_light = os.getenv('HUE_LIGHT')

endpoint  = 'http://%s/api/%s/lights/%s' % (hue_ip, hue_user, hue_light)

state = requests.get(endpoint).json()['state']
ct  = state['ct']
bri = state['bri']

print "starting sunset"

while bri > 0:
    bri -= 1
    if ct < 452:
        ct += 3
    if ct >= 452:
        ct = 454
    print 'Brightness: %s, Color Temperature: %s' % (bri, ct)
    requests.put(endpoint + '/state', data = json.dumps({'on': True, 'bri': bri, 'ct': ct}))
    time.sleep(4)

requests.put(endpoint + '/state', data = json.dumps({'on': False}))

print "done"
