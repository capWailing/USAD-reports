import requests
import os
import time
import re

URL = "https://mymarketnews.ams.usda.gov/services/v1/public/listPublishedReports"
URL_ROOT = "https://mymarketnews.ams.usda.gov"
URL_FILE = "https://mymarketnews.ams.usda.gov/filerepo/reports?field_slug_id_value=&name=%s&field_slug_title_value=" \
           "&field_published_date_value=&field_report_date_end_value=%s&field_api_market_types_target_id=All"
PATH = "/Users/zituoyan/PycharmProjects/USDA-reports/files"
DATE_TODAY = time.strftime("%Y-%m-%d", time.localtime())


# search the folder list all files
def get_file_names(path):
    name_list = [names[0:names.index('.')] for names in os.listdir(path)]
    return name_list


# get today's report slug name list
# return list
def list_today_reports():
    print("entering list today reports function")
    response = requests.get(URL)
    result = response.json()
    report_list = result.splitlines(False)
    report_slug_names = []
    for report in report_list:
        columns = report.split()
        if len(columns) > 1 and columns[0].isdigit():
            report_slug_names.append(columns[1])
    print("exit list today reports function")
    print(report_slug_names)
    return report_slug_names


# get file addresses from search page
# return list
def get_file_address(slug_names):
    print("entering get file address function")
    current_url = URL_FILE % (slug_names, DATE_TODAY)
    response = requests.get(current_url)
    result_list = []
    if response.status_code == 200:
        for line in response.content.decode("utf-8").splitlines():
            if "view report" in line:
                p1 = re.compile(r"href=\".*?\"", re.S)
                result = re.findall(p1, line)[0][6:-1]
                result_list.append(result)
    print("exit get file address function")
    print(result_list)
    return result_list


# extract file name from file url
# return string
def file_name_from_url(file_url):
    for offset, ch in enumerate(file_url[::-1]):
        if ch == '/':
            return file_url[-offset:]


# download file in the file list of single slug name i.e. or_fv150
# this might be a list because there could be multiple files in one slug name per day
def download_list(file_list):
    print("entering download list function")
    for file in file_list:
        url = URL_ROOT + file
        print(url)
        r = requests.get(url)
        with open("/Users/zituoyan/PycharmProjects/USDA-reports/files" + file_name_from_url(file), 'wb') as f:
            f.write(r.content)


# download all the reports list in the current index
def download_files():
    for slug_name in list_today_reports():
        download_list(get_file_address(slug_name))
    # download_list(get_file_address(list_today_reports()))
    # get_file_address('ams_2771')


if __name__ == '__main__':
    download_files()
