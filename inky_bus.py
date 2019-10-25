import requests


resp = requests.get('https://api.tfl.gov.uk/StopPoint/490007732N/arrivals')
if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
for bus in resp.json():
    
    minutes = bus['timeToStation']//60
    seconds = bus['timeToStation']%60
    print('{} {:02d}mins {:02d}secs {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']))
   