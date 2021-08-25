import requests
from requests.auth import HTTPBasicAuth
import json


def get_file():
    API_ENDPOINT = "https://marsapi.ams.usda.gov/services/v1/reports/"
    API_KEY = "h3bYbJ7SsUYCcg353GV+jjOhYc9XngZ6"
    response = requests.get(API_ENDPOINT, auth=HTTPBasicAuth(API_KEY, ""))
    print(response.json())
    result = []
    for i in response.json():
        new = i["slug_id"]
        result.append(new)
    print(result)


if __name__ == '__main__':
    get_file()
