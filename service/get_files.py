import requests
from requests.auth import HTTPBasicAuth
import json


def get_file():
    API_ENDPOINT = "https://marsapi.ams.usda.gov/services/v1.2/reports/2017"
    API_KEY = "h3bYbJ7SsUYCcg353GV+jjOhYc9XngZ6"
    response = requests.get(API_ENDPOINT, auth=HTTPBasicAuth(API_KEY, ""))
    print(response.text)


if __name__ == '__main__':
    get_file()
