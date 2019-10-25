import requests
from datetime import datetime

resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for bus in resp.json():
    print(datetime.fromisoformat(bus['expectedArrival']))
    print('{} {}'.format(bus['expectedArrival'], bus['lineName']))
    #print('{} {}'.format(bus['lineName']))
    #print('Bus - {}'.format(bus['lineNumber']))