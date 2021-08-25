import requests

URL = "localhost:9200/usda_reports"


def get_report_by_id(es_id):
    response = requests.get(URL + "/" + es_id)
    print(response)


