#!/usr/bin/env python

import os
import subprocess
import shlex
import time
import glob
import re
from pprint import pprint

ctrl_iface="wlan0"
pwn_iface="wlan1"
tmpfile="/tmp/airstrike"

friendly_skies = ["rednet"]

def do(commandline):
	args = shlex.split(commandline)
	pprint(args)
	p = subprocess.Popen(args)
	return p

def down(iface):
	p = do("ifconfig %s down" % iface)
	p.wait()
	
def scan(sleep_time):
	p = do("airodump-ng --output-format csv -w %s %s" % (tmpfile, pwn_iface))

	time.sleep(sleep_time)
	p.terminate()
	time.sleep(1)
	p.kill()

down(pwn_iface)

#scan(15)



def friendly(line):
	for f in friendly_skies:
		if line.find(f) != -1:
			return True
	return False

def aim():
	files = glob.glob("%s*.csv" % tmpfile)
	targets = []

	for f in files:
		fp = open(f, 'r')
	
		# Filter off the header lines
		lines = [x.strip(' \r\n') for x in list(fp)[2:]]
	
		# stop at the first blank line, just before stations
		lines = lines[:lines.index('')]
	
		# now we have a list of BSSIDs only.
		# Now filter out friendlies
		filtered = filter(lambda x: not friendly(x), lines)
		
		targets.extend(filtered)
		
	
	# targets is our list of targets to poke at now
	
	
	
	

