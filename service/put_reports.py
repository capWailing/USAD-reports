import requests
import time

URL = "localhost:9200/usda_reports"
DOC = "/_doc"
DATE_TODAY = time.strftime("%m-%d-%Y %I:%M:%S %p", time.localtime())


def put_report(slug_id, slug_name, report_title, publish_date, report_date, document):
    param = {"slug-id": slug_id,
             "slug-name": slug_name,
             "report-title": report_title,
             "publish-date": publish_date,
             "report-date": report_date,
             "document": document,
             "pull-date": DATE_TODAY}
    response = requests.post(URL + DOC + "/", json=param)
    print(response.json())


if __name__ == '__main__':
    put_report()