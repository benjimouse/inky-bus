import requests


resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
if resp.status_code != 200:
    raise ApiError('GET /arrivals/ {}'.format(resp.status_code))
sortedArrival = resp.json()
sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
for bus in sortedArrival:
    
    minutes = bus['timeToStation']//60
    seconds = bus['timeToStation']%60
    print('{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']))
   
