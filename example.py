from uk_covid19 import Cov19API

england_only = [
    'areaType=nation',
    'areaName=England',
    'date=2020-09-22'
]

cases_and_deaths = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeathsByDeathDate": "newDeaths28DaysByDeathDate",
    "cumDeathsByDeathDate": "cumDeaths28DaysByDeathDate"
}

api = Cov19API(filters=england_only, structure=cases_and_deaths)

data = api.get_json()

print(data)