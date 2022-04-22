import json
import requests
import random
import pytz 
from dateutil.parser import parser, isoparse
from datetime import datetime, timezone


def getDetails(endPoint, code):
    resp = requests.get(endPoint.format(code))
    if resp.status_code != 200:
        print('Failed - {}'.format(resp.status_code))
        print('{}'.format(resp.text))

    if code == "":
        details = resp.json()[random.randint(0,len(resp.json())-1)]
    else:
        details = resp.json()

    return details

def getOutput(endPoint, code):
    d = datetime.now()
    timezone = pytz.timezone("Europe/London")
    d_aware = timezone.localize(d)
    details = getDetails(endPoint, code)
    output = {}
    output['header'] = '{}'.format(d_aware.strftime('%Y-%m-%d %H:%M'))
    output['subHeader'] = '{}'.format(details['country'])
    output['body'] = ''
    output['body'] = output['body'] +   '         Total    Today'
    output['body'] = output['body'] + '\nCases:  {}   {}'.format('{:,}'.format(details['cases']).rjust(6), '{:,}'.format(details['todayCases']).rjust(6))
    output['body'] = output['body'] + '\nDeaths: {}   {}'.format('{:,}'.format(details['deaths']).rjust(6), '{:,}'.format(details['todayDeaths']).rjust(6))
    output['body'] = output['body'] + '\nPer million'
    output['body'] = output['body'] + '\nCases:  {} Deaths: {}'.format('{:,}'.format(details['casesPerOneMillion']).rjust(6), '{:,}'.format(details['deathsPerOneMillion']).rjust(6))
    output['body'] = output['body'] + '\nRecovered: {}'.format('{:,}'.format(details['recovered']).rjust(6))
    output['bodyLines'] = 6
    return output
    
