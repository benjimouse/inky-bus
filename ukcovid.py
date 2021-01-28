import json
import requests
import random
import pytz 
from dateutil.parser import parser, isoparse
from datetime import datetime, timezone
from uk_covid19 import Cov19API


def getDetails(endPoint, code):

    currDate = '{}'.format(datetime.today().strftime('%Y-%m-%d'))
    
    filters = [
        'areaType=nation',
        'areaName=England',
        
    ]

    cases_and_deaths = {
        "date": "date",
        "newAdmissions": "newAdmissions",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "newDeathsByDeathDate": "newDeaths28DaysByDeathDate",
    }

    api = Cov19API(filters=filters, structure=cases_and_deaths, latest_by="newAdmissions")

    data = api.get_json()

    return data

def getOutput(endPoint, code):
    print(endPoint)
    details = getDetails(endPoint, code)
    print(details)

    # d = datetime.now()
    # timezone = pytz.timezone("Europe/London")
    # d_aware = timezone.localize(d)
    output = {}
    # output['header'] = '{}'.format(d_aware.strftime('%Y-%m-%d %H:%M'))
    # output['subHeader'] = '{}'.format(details['country'])
    # output['body'] = ''
    # output['body'] = output['body'] +   '         Total    Today'
    # output['body'] = output['body'] + '\nCases:  {}   {}'.format('{}'.format(details['cases']).rjust(6), '{}'.format(details['todayCases']).rjust(6))
    # output['body'] = output['body'] + '\nDeaths: {}   {}'.format('{}'.format(details['deaths']).rjust(6), '{}'.format(details['todayDeaths']).rjust(6))
    # output['body'] = output['body'] + '\nPer million'
    # output['body'] = output['body'] + '\nCases:  {} Deaths: {}'.format('{}'.format(details['casesPerOneMillion']).rjust(6), '{}'.format(details['deathsPerOneMillion']).rjust(6))
    # output['body'] = output['body'] + '\nRecovered: {}'.format('{}'.format(details['recovered']).rjust(6))
    # output['bodyLines'] = 6
    return output
    
