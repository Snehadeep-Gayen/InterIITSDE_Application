'''
Run this with the input sequence of computes:
Example:
aaabbcbdbcbd
to request the microservices in that order.
Each microservice will be send a query every 1 second
and output of monitor will be displyed to screen
'''

import requests
import time
import sys

url = { 'a': 'http://localhost:5000/compute', \
        'b': 'http://localhost:5001/compute', \
        'c': 'http://localhost:5002/compute', \
        'd': 'http://localhost:5003/compute' }

monitor_url = 'http://localhost:9090/'

input = 2

def request_result(c):
    return requests.get(url[c], params={'input': input}).json()['output']

def request_monitor():
    return requests.get(monitor_url).json()

def display_monitor():
    # pretty print monitor
    # print(request_monitor())
    myjson = request_monitor()
    # print ready_queue, slopes, and ping times for each microservice
    print(f'Ready Queue: {myjson["ready_queue"]}')
    print(f'Slopes: {myjson["slope"]}')
    print(f'Ping Times: {myjson["pings"]}')

if __name__ == '__main__':
    display_monitor()
    for c in sys.argv[1]:
        print(f'Requesting {c}...')
        print(f'Result: {request_result(c)}')
        display_monitor()
        time.sleep(1)