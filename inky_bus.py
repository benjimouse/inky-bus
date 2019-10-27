import requests
from datetime import datetime, timezone
from dateutil.parser import parser, isoparse

reRunTime = datetime.now(timezone.utc)

def get_bus_time():
    resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
    if resp.status_code != 200:
        raise ApiError('GET /arrivals/ {}'.format(resp.status_code))
    sortedArrival = resp.json()
    sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
    
    reRunTime = isoparse(sortedArrival[0]['timeToLive'])
    print('{}'.format(reRunTime))
    for bus in sortedArrival:
        if isoparse(bus['timeToLive']) < reRunTime:
            reRunTime = isoparse(bus['timeToLive'])
            

        minutes = bus['timeToStation']//60
        seconds = bus['timeToStation']%60
        print('{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']))
        print('time to live {}'.format(isoparse(bus['timeToLive'])))
    

get_bus_time()