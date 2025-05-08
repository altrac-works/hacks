#!/usr/bin/env python3

import json
import sys
import requests
import random
import time
import socket

with open('diffbot3000.config.json', 'r') as f:
    config = json.load(f)
    hook_url = config["hook_url"]

mode = sys.argv[1]
thing = sys.argv[2]
previous = None
current = None
first_check = True

while True:
    try:
        #do the diff
        if mode == "http-modified":
            response = requests.head(thing)
            current = response.headers['Last-Modified']
        else:
            sys.exit("I don't know how to watch that")
    except Exception as e:
        print("Failure while checking")
        logging.error(traceback.format_exc())
    
    print("Was", previous, "Now", current)
    
    try:
        if current != previous and first_check == False:
            #do stuff
            hook_content = '*Updates to ' + thing + '* (checking in mode ' + mode + ')\n*Was:* ' + str(previous) + '\n*Now:* ' + str(current)
    
            hook_body = {"username":"diffbot3000 on " + socket.gethostname(), "content": hook_content}
            hook_result = requests.post(hook_url, json=hook_body)
            try:
                hook_result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print(f"Payload delivered successfully, code {hook_result.status_code}.")
            
            first_check = False
    except Exception as e:
        print("Error while notifying")
        logging.error(traceback.format_exc())

    previous = current
    time.sleep(random.randint(300, 600))


