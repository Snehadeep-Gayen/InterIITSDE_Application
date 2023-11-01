from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# this is the monitor microservice
pings = {}
ready_queue = []
url = {}

# for computation
rate_of_slope = {}
slope = {}
x = {}
restart_time = 10
capacity = 0.20

# redirect
def turn_on_redirect(microservice_url):
    return jsonify(requests.get(f'{microservice_url}/redirect').json())

def check_redirect(microservice):
    if len(pings[microservice]) < 2:
        return
    elif len(pings[microservice]) == 2:
        x[microservice] = (pings[microservice][1] + pings[microservice][0])/2
        slope[microservice] = 1/(pings[microservice][1] - pings[microservice][0])
        return
    else:

        x2 = (pings[microservice][-1] + pings[microservice][-2])/2
        m2 = 1/(pings[microservice][-1] - pings[microservice][-2])
        # take average 
        m1 = slope[microservice]
        x1 = x[microservice]
        # recompute (check md file for details)
        slope[microservice] = (m1 + m2)/2
        x[microservice] = (x1 + x2)/2
        rate_of_slope[microservice] = (m2 - m1)/(x2 - x1)

    # if the projected rate of requests at current time
    # is greater than 1-1/n, redirect

    n = len(ready_queue)

    max_cap = (1 - 1/n) * capacity
    if n == 1:
        max_cap = capacity

    if slope[microservice] > max_cap:
        ready_queue.remove(microservice)
        turn_on_redirect(url[microservice])
        return
    
    time_needed = (max_cap - slope[microservice])/rate_of_slope[microservice]
    if time_needed > 0 and time_needed < restart_time/2:
        ready_queue.remove(microservice)
        turn_on_redirect(url[microservice])

# receive the POST request from microservices
@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    microservice = data['microservice']
    if microservice in pings:
        pings[microservice].append(time.time())
    else:
        pings[microservice] = [time.time()]
    ready_queue.remove(microservice)
    ready_queue.append(microservice)
    check_redirect(microservice)
    return jsonify({'message': 'OK'})

# delegate the request to the microservice in the front of the ready queue
@app.route('/delegate', methods=['GET'])
def compute():
    input = request.args.get('input', 0)
    if len(ready_queue) > 0:
        microservice = ready_queue[0]
        return jsonify(requests.get(f'{url[microservice]}/compute?input={input}').json())
    else:
        return jsonify({'message': 'No microservice available'})

# register the microservice, its url, and its name
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    url[data['name']] = data['url']
    ready_queue.append(data['name'])
    return jsonify({'message': 'OK'})

# show the status of the monitor
@app.route('/')
def show_status():
    # return both pings and ready queue
    return jsonify({'pings': pings, 'ready_queue': ready_queue, \
        'url': url, 'rate_of_slope': rate_of_slope, 'slope': slope, 'x': x})

if __name__ == '__main__':
    pings = {}
    ready_queue = []
    url = {}
    rate_of_slope = {}
    slope = {}
    x = {}
    app.run(host='0.0.0.0', port=9090)
