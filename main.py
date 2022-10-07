import metro_routes
from flask import Flask 
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect

f = open('GTFS/metro_stations.txt', 'r')
metro_stations = f.read().split('\n')
f.close()

def check_metro_station_exists(stop): 
    for station in metro_stations: 
        if stop in station or station in stop:
            return station
    return False 

def least_interchanges(start_stop, end_stop):
    import bus_routes
    start_metro_station = check_metro_station_exists(start_stop) 
    end_metro_station = check_metro_station_exists(end_stop)

    if start_metro_station and end_metro_station:
        metro_route = metro_routes.get_data(start_metro_station, end_metro_station)

    bus_route = bus_routes.get_data(start_stop, end_stop)

    if bus_route and start_metro_station and end_metro_station: 
        if len(bus_route['path']) < len(metro_route['interchange']):
            return bus_route
        else:
            return metro_route

def fastest_route(start_stop, end_stop):
    import bus_routes
    bus_route = bus_routes.get_data(start_stop, end_stop)
    bus_path = bus_route['path']
    lowest_time = bus_route['time']
    lowest_time_path = bus_route
    i = 0 
    while i < len(bus_path) - 1: 
        j = len(bus_path) - 1
        while j > i: 
            start_metro_station = check_metro_station_exists(bus_path[i])
            end_metro_station = check_metro_station_exists(bus_path[j])
            time = 0.0
            current_time_path = []
            if start_metro_station and end_metro_station: 
                bus_path_1 = bus_path[0:i+1]
                bus_path_2 = bus_path[j:len(bus_path)]
                metro_path = [start_metro_station, end_metro_station]

                bus_route_1 = {} 
                bus_route_2 = {}
                if len(bus_path_1) > 1:
                    bus_route_1 = bus_routes.get_data(bus_path_1[0], bus_path_1[-1])

                if len(bus_path_2) > 1:            
                    bus_route_2 = bus_routes.get_data(bus_path_2[0], bus_path_2[-1])
                
                metro_route = metro_routes.get_data(metro_path[0], metro_path[1])

                time = (bus_route_1.get('time') or 0) + (bus_route_2.get('time') or 0) + metro_route['time']
                current_time_path = [bus_route_1, metro_route, bus_route_2]
            
            if time < lowest_time and time != 0.0: 
                lowest_time = time
                lowest_time_path = current_time_path

            j -= 1
        i += 1

    return lowest_time_path

def lowest_cost_route(start_stop, end_stop):
    import bus_routes
    bus_route = bus_routes.get_data(start_stop, end_stop)
    bus_path = bus_route['path']
    lowest_cost = bus_route['fare']
    lowest_cost_path = bus_route
    i = 0
    while i < len(bus_path) - 1: 
        j = len(bus_path) - 1
        while j > i: 
            start_metro_station = check_metro_station_exists(bus_path[i])
            end_metro_station = check_metro_station_exists(bus_path[j])
            cost = 0.0
            current_cost_path = []

            if start_metro_station and end_metro_station: 
                bus_path_1 = bus_path[0:i+1]
                bus_path_2 = bus_path[j:len(bus_path)]
                metro_path = [start_metro_station, end_metro_station]

                bus_route_1 = {} 
                bus_route_2 = {}
                if len(bus_path_1) > 1:
                    bus_route_1 = bus_routes.get_data(bus_path_1[0], bus_path_1[-1])

                if len(bus_path_2) > 1:            
                    bus_route_2 = bus_routes.get_data(bus_path_2[0], bus_path_2[-1])
                
                metro_route = metro_routes.get_data(metro_path[0], metro_path[1])

                if type(metro_route['fare']) == str: 
                    cost = (bus_route_1.get('fare') or 0) + (bus_route_2.get('fare') or 0) + int(metro_route.get('fare'))
                elif type(metro_route['fare']) == list: 
                    cost = (bus_route_1.get('fare') or 0) + (bus_route_2.get('fare') or 0) + int(metro_route.get('fare')[-1])
                current_cost_path = [bus_route_1, metro_route, bus_route_2]

            if cost < lowest_cost and cost != 0.0:
                lowest_cost = cost 
                lowest_cost_path = current_cost_path
            j -= 1
        i += 1

    return lowest_cost_path

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.php')

@app.route('/blog.php')
def blog():
    return render_template('blog.php')

@app.route('/brand.php')
def brand():
    return render_template('brand.php')
route = None
l = False 
@app.route('/get-data', methods=['POST', 'GET'])
def get_data(): 
    if request.method == 'POST':
        val = request.form['type']
        start = request.form['from']
        end = request.form['to']
        global route
        global l 
        print(val)
        if val == 'volvo': 
            route = fastest_route(start, end)
            l = False
        elif val == 'saab':
            route = lowest_cost_route(start, end)
            l = False 
        elif val == 'mercedes':
            route = least_interchanges(start, end)
            l = True
        if type(route) == dict:
            l = True 
        else: 
            l = False
        return redirect('/get-data')
    else: 
        print(route)
        return render_template('recieve.php', path=route, least_interchanges=l)

    
