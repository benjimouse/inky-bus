import json
import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def getCountryDetails(countryEndPoint, countryCode):
    sample_transport=RequestsHTTPTransport(
        url=countryEndPoint,
        use_json=True,
        headers={
            "Content-type": "application/json",
        },
        verify=False
    )

    client = Client(
        retries=3,
        transport=sample_transport,
        fetch_schema_from_transport=True,
    )

    query = gql('''
        query {
    country(code:"''' + countryCode + '''")
    {
        name,
        emoji,
        emojiU
    }
    }
    ''')

    return client.execute(query)['country']

def mapCountryToOutput(countryDetails):
    output = {}
    output['header'] = '{}'.format(countryDetails['name'])
    output['subHeader'] = ''
    output['body'] = '{}'.format(countryDetails['emojiU'])
    output['bodyLines'] = 1
    return output

def getOutput(endPoint, code):
    return mapCountryToOutput(getCountryDetails(endPoint, code))