import requests
import time

def callServiceGet(url):
    r = requests.get(url)
    print(r.status_code)

    #r.status_code == requests.codes.ok

def callServicePost(url, data):
    r = requests.post(url, json=data)
    print(r.status_code, r.reason)

def callNeo4JSchedule(url, data, method):
    while True:
        #match first. if node/relationship exists, then update or ignore othewise create
        callServicePost(url, data)
        time.sleep(300)

def deleteAllNodes(url="", method="get"):
    callServiceGet(url, method)