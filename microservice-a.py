from flask import Flask, request, jsonify, json
import requests

app = Flask(__name__)

microservice_name = 'microservice-a'
my_url = 'http://localhost:5000'
requests_processed = 0
redirect = False

############# EXTRA FUNCTIONS FOR MONITOR ################

monitor_url = 'http://localhost:9090'

def notify_monitor():
    requests.post(monitor_url + '/notify', json={'microservice': microservice_name})

@app.route('/alive', methods=['GET'])
def alive():
    return jsonify({'message': 'I\'m alive!'})

@app.route('/redirect', methods=['GET'])
def redirect():
    global redirect
    redirect = True
    return jsonify({'message': 'Redirecting...'})

def register():
    requests.post(monitor_url + '/register', json={'name': microservice_name, 'url': my_url})

##########################################################

@app.route('/wake', methods=['GET'])
def wake():
    register()
    global requests_processed
    global redirect
    redirect = 0
    requests_processed = 0
    return jsonify({'message': 'I\'m awake!'})

@app.route('/compute', methods=['GET'])
def compute(): # finds the 2^i iteratively input
    global requests_processed
    requests_processed += 1
    input = request.args.get('input', 0)
    ######### ADDED FOR MONITOR ##########
    notify_monitor()
    global redirect
    if(redirect):
        return requests.get(f'{monitor_url}/delegate?input={input}').json()
    ######################################
    input = int(input)
    output = 1
    for i in range(input):
        output *= 2
    return jsonify({'output': output})

@app.route('/')
def hello_world():
    global requests_processed
    return jsonify({'message': 'Hello, I\'m microA at your service!' + \
        f' \n Requests processed: {requests_processed} '})

if __name__ == '__main__':
    requests_processed = 0
    redirect = 0
    #### ADDED FOR MONITOR ####
    register()
    ###########################
    app.run(host='0.0.0.0', port=5000)
