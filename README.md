# INTER-IIT SDE Application

## Personal Details

**Name : Snehadeep Gayen**
**Roll Number : CS21B078**
**CGPA : 9.90**
**LinkedIn Profile : [https://www.linkedin.com/in/snehadeep-gayen/](https://www.linkedin.com/in/snehadeep-gayen/)**

## Monitor Application

Horizontal scaling is the process of adding more instances of a microservice to handle increased workload. This project develops a monitor that can 

1. <u> Monitor the parameters </u> of a microservice
2. <u> Balance Load </u> from a heavily used node to a less used node, allowing the heavily used node to restart and recover
3. <u> Make predictions </u> about the future load on the microservice (An _Online Quadratic-Fitting Algorithm_ is used in this case)

## Architecture

![Architecture](img/architecture.png)

## Prediction Algorithm

For each node, the following time-series data is stored <i> (One can store only the last data for space optimisation $ \mathcal{O}(1) $ space solution) </i>

1. $ p_i $ : The time at which the $ i^{th} $ request was received
2. $ x_i $ : Which is $ {(p_i + p_{i-1})}/{2} $, the middle time between the $ i^{th} $ and $ (i-1)^{th} $ request
3. $ slope_i $ : computed slope at $ x_i $ which is average of $ slope_{i-1} $ and $ 1/(p_i - p_{i-1}) $
4. $ rate_i $ : computed rate of change of slope at $ (x_i + x_{i-1})/2 $ which is $ (slope_i - slope_{i-1})/(p_i - p_{i-1}) $

Let `capacity` denote the maximum rate of requests that each server can handle,
`n` be the number of available nodes at the moment and
`restart_time` denote the time taken to restart a node.

Then, a node should be restarted if 

$$
    time\_to\_exceed = \frac{(capacity*(1-1/n) - slope_i)}{rate_i} < restart\_time
$$

When a node is being restarted <i> (Restarting of node hasn't been implemented in this project) </i>, its requests are distributed among the other **active** nodes.

## Usage

1. Clone the repository 
2. Run `python monitor.py` to start the monitor (Install the dependencies if prompted)
3. Run the 4 microservices in 4 different terminals using `python microservice-{character}.py` where `{character}` is of `a`, `b`, `c` and `d`. (Again, install the required dependencies if prompted)
4. Next run the script file `python script.py {Ping_sequence}` to send requests to the microservices. The script requests to the microservices in the order specified by the `{Ping_sequence}` argument. For example, `python script.py abcd` will send requests to microservice `a` first, then to `b`, then to `c` and finally to `d`.  The script will also print the response and the state of the monitor for each request.

### Parameters that can be changed to experiment

1. `sleep_time` in `script.py` can be changed to change the time between two consecutive requests.
2. `capacity` in `monitor.py` can be changed to change the maximum rate of requests that each server can handle (in $Hz$).
3. `restart_time` in `monitor.py` can be changed to change the time taken to restart a node (in $s$).


## Note:
HTML pages, CSS sheets haven't been implemented because of insufficient time. The requests currently return JSON objects (which have been pretty printed in the script).
