import requests
from datetime import datetime, timezone
from dateutil.parser import parser, isoparse

resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
if resp.status_code != 200:
    raise ApiError('GET /arrivals/ {}'.format(resp.status_code))
sortedArrival = resp.json()
sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
reRunTime = datetime.now(timezone.utc)
print('{}'.format(reRunTime))
for bus in sortedArrival:
   # if datetime.fromisoformat(bus['timeToLive']) < reRunTime
    #    reRunTime = parser.parse(bus['timeToLive'])

    minutes = bus['timeToStation']//60
    seconds = bus['timeToStation']%60
    print('{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']))
    print('time to live {}'.format(isoparse(bus['timeToLive'])))
   
