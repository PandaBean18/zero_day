# { 
#     origin_stop_id => { 
#         destination_stop_1_id => {
#             fare_id => fare_id, 
#             route_id => route_id
#         } 
#     } 
# } 

# Code used to arrange the routes data as a graph
import pickle

h = {}

read_obj = open('GTFS/fare_rules.txt', 'r')

read_obj.readline()

data = read_obj.readlines()
stops_left = ['0']
while len(stops_left) > 0: 
    current_origin_stop_id = stops_left[0]
    print(stops_left)
    for datum in data: 
        rec = datum[0:-1].split(',')
        stops_completed = h.keys()
        if rec[2] == current_origin_stop_id:
            if not h.get(rec[2]):
                h[rec[2]] = {}
                h[rec[2]][rec[3]] = {
                    'fare_id': rec[0],
                    'route_id': rec[1]
                } 
            else: 
                h[rec[2]][rec[3]] = {
                    'fare_id': rec[0],
                    'route_id': rec[1]
                }

            if rec[3] not in stops_completed:
                stops_left.append(rec[3])

    stops_left.pop(0)


read_obj.close()
write_obj = open('tree.bin', 'wb')

pickle.dump(h, write_obj)
write_obj.close()