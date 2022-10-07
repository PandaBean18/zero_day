# t[(t.index('Token Fare')+78):t.index('Token Fare')+78+38]

import requests 
import json 

session = requests.Session()

def get_path(start_stop, end_stop):
    start = start_stop.lower().split(' ')
    end = end_stop.lower().split(' ')
    data = session.get(f"https://delhimetroapi.herokuapp.com/metroapi/from={'%20'.join(start)}&to={'%20'.join(end)}")
    json_obj = data.text
    path = json.loads(json_obj)
    return path 

def calc_fare(start_stop, end_stop):
    start = start_stop.lower().split(' ')
    end = end_stop.lower().split(' ')
    data = session.get(f"https://yometro.com/from-{'-'.join(start)}-metro-station-delhi-to-{'-'.join(end)}-metro-station-delhi")
    text = data.text
    idx = text.index('Token Fare') + 78 
    fare = text[idx:idx+38]
    if 'Airport' not in fare: 
        fare = fare.split(' ')[0]
    else: 
        fare = [fare.split(' ')[0], fare.split(' ')[3]]
    return fare

def get_data(start_stop, end_stop):
    metro_data = get_path(start_stop, end_stop)
    lines = []
    interchange = metro_data.get('interchange') or []
    path = metro_data['path']
    time = metro_data['time']
    fare = calc_fare(start_stop, end_stop)
    if type(fare) == list: 
        fare = int(fare[1])
    else: 
        fare = int(fare)
        
    for key in metro_data:
        if 'line' in key and key != 'lineEnds':
            for line in metro_data[key]:
                if line not in lines:
                    lines.append(line)

    h = {
        'path': path, 
        'lines': lines, 
        'interchange': interchange, 
        'fare': fare, 
        'time': time
    }

    return h

