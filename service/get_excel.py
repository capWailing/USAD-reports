import os

import xlrd
import requests
import logging

URL = "https://marketnews.usda.gov/mnp/fv-report"
parameter = {"repType": "",
             "type": "",
             "repTypeChanger": "",
             "locName": "",
             "locAbr": "",
             "locChoose": "",
             "commodityClass": "",
             "organic": "",
             "repDate": "",
             "endDate": "",
             "format": "",
             "_environment": "",
             "rebuild": ""}
re_download_list = []


def download_excel(result_dict):
    response = requests.get(URL, params=result_dict)
    size = response.headers["Content-Length"]
    logging.info(response.url)
    logging.info("File size should be:" + str(size))
    file_path = "/Users/zituoyan/PycharmProjects/USDA-reports/files/" + result_dict["repDate"].replace("%2F", "-") + \
                result_dict["locAbr"] + ".xls"
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        if int(file_size) == int(size):
            logging.warning("File exists, not retrieving.")
            return True
        else:
            logging.warning("File size should be:" + str(size) + ", but actually is:" + str(file_size) +
                            ", re-download started.")
            with open(file_path, 'wb') as f:
                f.write(response.content)
                logging.info("Download complete!")
            result = verification(file_path, size, result_dict)
            return result
    else:
        with open(file_path, 'wb') as f:
            f.write(response.content)
            logging.info("Download complete!")
        result = verification(file_path, size, result_dict)
        return result


def download_excel_p(rep_type, type_a, rep_type_changer, loc_name, loc_abr, loc_choose, commodity_class, organic, rep_date,
                   end_date, format_type, environment, rebuild):
    logging.info("Entering method build requests.")
    parameter_list = [rep_type, type_a, rep_type_changer, loc_name, loc_abr, loc_choose, commodity_class, organic,
                      rep_date, end_date, format_type, environment, rebuild]
    result_dict = dict(zip(parameter.keys(), parameter_list))
    download_excel(result_dict)


def verification(file_path, size, result_dict):
    file_size = os.path.getsize(file_path)
    logging.info("File size actually:" + str(file_size))
    if int(file_size) != int(size):
        logging.warning("File size should be:" + str(size) + ", but actually is:" + str(file_size) +
                        ", add into re-download list.")
        re_download_list.append(result_dict)
        return False
    else:
        return True


def retry():
    download_list = re_download_list.copy()
    if re_download_list:
        for file in re_download_list:
            logging.info("Re-downloading:" + file["repDate"] + file["locAbr"])
            result = download_excel(file)
            if result:
                download_list.remove(file)
                logging.info("Re-download success.")
            else:
                logging.warning("Re-download fail.")
    if len(download_list) == 0:
        logging.info("Re-download complete")
    else:
        for file in download_list:
            logging.warning("File " + file["repDate"] + file["locAbr"] + " re-download fail.")


if __name__ == '__main__':
    logging.basicConfig(filename='download.log', level=logging.INFO)
    logging.info("Started")
    download_excel_p("termPriceDaily", "termPrice", "termPriceDaily", "LOS+ANGELES", "HC", "location", "allcommodity",
                   "", "09%2F01%2F2021", "09%2F01%2F2021", "excel", "1", "false")
    retry()
    logging.info("Finished")
