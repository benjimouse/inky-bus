import json
import os
import requests
from dateutil.parser import parser, isoparse
from datetime import datetime, timezone


def getBusTime(stopEndPoint, stop):
    resp = requests.get(stopEndPoint.format(stop))
    if resp.status_code != 200:
        print('Failed - {}'.format(resp.status_code))
        print('{}'.format(resp.text))

    sortedArrival = resp.json()
    sortedArrival.sort(key=lambda k: k['timeToStation'], reverse=False)
    arrivals = []
    for bus in sortedArrival:
        bus_arrival = {}
        bus_arrival['timeToStation'] = bus['timeToStation']
        bus_arrival['lineName'] = bus['lineName']
        bus_arrival['ttl'] = isoparse(bus['timeToLive'])
        bus_arrival['destinationName'] = bus['destinationName']
        bus_arrival['stopName'] = bus['stationName']
        bus_arrival['stopCode'] = bus['platformName']
        arrivals.append(bus_arrival)

    return arrivals

def mapBusTimesToOutput(busTimes):
    output = {}
    output['header'] = '{}'.format(datetime.now(timezone.utc).strftime('%H:%M:%S'))
    output['subHeader'] = '{} busses'.format(len(busTimes))
    output['body'] = ''
    output['bodyLines'] = len(busTimes)
    if len(busTimes) > 0:
        output['header'] = output['header'] + ' {} {}'.format(busTimes[0]['stopName'], busTimes[0]['stopCode'])
        output['body'] = output['body'] + formatArrivals(busTimes)

    return output
    
def formatArrivals(arrivals):
    message = ''
    for bus in arrivals:

        minutes = bus['timeToStation']//60
        seconds = bus['timeToStation']%60
        message = message + '{} {:02d}m{:02d}s {}'.format(bus['lineName'], minutes, seconds, bus['destinationName']) + '\n'
    
    return message

def getOutput(endPoint, code):
    return mapBusTimesToOutput(getBusTime(endPoint, code))