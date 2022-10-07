import pickle

f = open('tree.bin', 'rb')
h = pickle.load(f)
f.close()

f = open('GTFS/stops.txt', 'r')
f.readline()
stops_data =  f.read().split('\n')
f.close()

f = open('GTFS/fare_attributes.txt', 'r')
f.readline()
fare_data = f.read().split('\n')
f.close()

f = open('GTFS/trips.txt', 'r')
f.readline()
trips_data = f.read().split('\n')
f.close()

f = open('GTFS/stop_times.txt', 'r')
f.readline()
stop_times_data = f.read().split('\n')
f.close()

backtrack = []
paths_traversed = []

def bsearch(stop_id):
    data_dup = stops_data.copy()
    current_idx = int(stop_id)
    while len(data_dup) > 0:
        rec = data_dup[current_idx].split(',')
        if rec[0] == stop_id:
            return rec
        elif int(rec[0]) > int(stop_id):
            data_dup = data_dup[0:current_idx]
        elif int(rec[0]) < int(stop_id):
            data_dup[0:current_idx+1] = []

        current_idx = len(data_dup) // 2

def path_to_zero(stop):
    global backtrack
    global paths_traversed
    backtrack = backtrack or [stop]
    stop_node = h.get(stop)
    if not stop_node: 
        paths_traversed.append(stop)
        return False

    child_nodes = h.get(stop).keys()
    child_nodes_not_traversed = []
    for child in child_nodes: 
        if child not in paths_traversed:
            child_nodes_not_traversed.append(child)

    if not child_nodes_not_traversed:
        paths_traversed.append(stop)
        return False 

    for child in child_nodes_not_traversed: 
        if (child in backtrack): 
            paths_traversed.append(child)
            continue
        backtrack.append(child)
        if child == '0': 
            return backtrack
        
        child_path = path_to_zero(child)

        if child_path: 
            return backtrack 
        
        backtrack.pop()
    paths_traversed.append(stop)
    return False


def find_shortest_path(origin_stop, end_stop):
    global backtrack
    global paths_traversed
    origin_stop_id = None
    end_stop_id = None
    for datum in stops_data:
        rec = datum.split(',')
        if origin_stop in rec[2] and not origin_stop_id:
            origin_stop_id = rec[0]
        elif end_stop in rec[2] and not end_stop_id:
            end_stop_id = rec[0]

        if origin_stop_id and end_stop_id:
            break

    path_start = path_to_zero(origin_stop_id)
    backtrack = []
    paths_traversed = []
    i = 0
    while i < len(path_start):
        j = len(path_start) - 1
        while j > i:
            if path_start[j] in h[path_start[i]].keys():
                path_start[(i+1):j] = []
                j -= (j-(i+1))
            j -= 1
        i += 1
    path_end = [end_stop_id]

    while path_end[-1] != '0':
        for key in h.keys():
            if (path_end[-1] in h[key].keys()):
                path_end.append(key)
                break

    greatest_common_ancestor = None
    shorter_path = None
    longer_path = None
    i = 0

    if len(path_start) > len(path_end):
        shorter_path = path_end
        longer_path = path_start
    else:
        shorter_path = path_start
        longer_path = path_end

    while i < len(shorter_path):
        if shorter_path[i] in longer_path:
            greatest_common_ancestor = shorter_path[i]
            break

        i += 1

    shorter_path[(i+1):len(shorter_path)] = []
    longer_path[longer_path.index(greatest_common_ancestor):len(longer_path)] = []
    path = path_start + path_end[::-1]
    i = 0
    while i < len(path):
        j = len(path) - 1
        while j > i:
            if path[j] in h[path[i]].keys():
                path[(i+1):j] = []
                j -= (j-(i+1))
            j -= 1
        i += 1
    return path

def calc_fare(path):
    i = 0
    fare = 0.0
    while i < (len(path) - 1):
        fare_id = h[path[i]][path[i+1]]['fare_id']
        for datum in fare_data:
            rec = datum.split(',')
            if rec[0] == fare_id:
                fare += float(rec[1])
                break

        i += 1
    return fare

def calc_time(path):
    i = 0
    hours = 0
    minutes = 0
    seconds = 0
    while i < (len(path) - 1):
        route_id = h[path[i]][path[i+1]]['route_id']
        trip_id = None
        start_time = None 
        end_time = None 

        for trip in trips_data:
            rec = trip.split(',')
            if rec[0] == route_id:
                trip_id = rec[2]
                break 

        for stop_time in stop_times_data: 
            rec = stop_time.split(',')
            if rec[0] == trip_id and rec[3] == path[i+1]:
                end_time = rec[1].split(':')
            elif rec[0] == trip_id and rec[3] == path[i]:
                start_time = rec[2].split(':')

            if start_time and end_time:
                break 

        hours += int(end_time[0]) - int(start_time[0])
        minutes += int(end_time[1]) - int(start_time[1])
        seconds += int(end_time[2]) - int(start_time[2])
        
        i += 1
    return (60*hours)+minutes+(seconds/60)

def get_data(start_stop, end_stop):
    path = find_shortest_path(start_stop, end_stop)
    fare = calc_fare(path)
    time = calc_time(path)
    stops_path = []

    for x in path:
        stops_path.append(bsearch(x)[2])

    h = {
        'path': stops_path, 
        'fare': fare, 
        'time': time
    }

    return h 
