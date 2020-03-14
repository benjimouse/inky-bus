import json
import requests
import random
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
    details = getDetails(endPoint, code)
    output = {}
    output['header'] = '{}'.format(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M'))
    output['subHeader'] = '{}'.format(details['country'])
    output['body'] = ''
    output['body'] = output['body'] +   'Cases total:  {}'.format('{}'.format(details['cases']).rjust(6))
    output['body'] = output['body'] + '\nCases today:  {}'.format('{}'.format(details['todayCases']).rjust(6))
    output['body'] = output['body'] + '\nDeaths total: {}'.format('{}'.format(details['deaths']).rjust(6))
    output['body'] = output['body'] + '\nDeaths today: {}'.format('{}'.format(details['todayDeaths']).rjust(6))
    output['body'] = output['body'] + '\nCases / mil:  {}'.format('{}'.format(details['casesPerOneMillion']).rjust(6))
    output['body'] = output['body'] + '\nDeaths/ mil:  {}'.format('{}'.format(details['deathsPerOneMillion']).rjust(6))
    output['body'] = output['body'] + '\nRecovered:    {}'.format('{}'.format(details['recovered']).rjust(6))
    output['bodyLines'] = 7
    return output
    
