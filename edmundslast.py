# utf-8


import time
import requests
import csv
from bs4 import BeautifulSoup
import undetected_chromedriver as webdriver

co = webdriver.ChromeOptions()

co.add_argument('--disable-infobars')
co.add_argument('--disable-extensions')
co.add_argument('--profile-directory=Default')
co.add_argument("--incognito")
co.add_argument("--headless")
co.add_argument("--disable-plugins-discovery")
co.add_argument("--start-maximized")
co.add_argument("--no-sandbox")  # bypass OS security model
co.add_argument("--disable-dev-shm-usage")
co.add_argument("--disable-popup-blocking")
co.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/90.0.4430.212 Safari/537.36")
co.add_argument('--disable-blink-features=AutomationControlled')


def makelist(htmlstring):
    soup = BeautifulSoup(htmlstring)
    table = soup.find('section', attrs={'class': ''})
    com = []
    try:
        for idx in range(6):
            for row in table.find_all("tr")[1:]:
                col = row.find_all("td")
                if len(col) > 0:
                    temp = col[idx].contents[0]
                    try:
                        to_append = temp.contents[0]
                    except Exception as e:
                        to_append = temp
                    com.append(to_append)
    except:
        pass
    return com


def main():

    zipcode = "80202"
    miss_list = []
    output_file = str(zipcode) + "_output.csv"
    write_header = ["vehicle_year", "vehicle_make", "vehicle_model", "vehicle_style", "yr1_tax_credit", "yr1_insurance",
                    "yr1_maintenance", "yr1_repairs", "yr1_taxs_fees", "yr1_financing", "yr1_depreciation", "yr1_fuel",
                    "yr1_total", "yr2_tax_credit", "yr2_insurance", "yr2_maintenance", "yr2_repairs", "yr2_taxs_fees",
                    "yr2_financing", "yr2_depreciation", "yr2_fuel", "yr2_total", "yr3_tax_credit", "yr3_insurance",
                    "yr3_maintenance", "yr3_repairs", "yr3_taxs_fees", "yr3_financing", "yr3_depreciation", "yr3_fuel",
                    "yr3_total", "yr4_tax_credit", "yr4_insurance", "yr4_maintenance", "yr4_repairs", "yr4_taxs_fees",
                    "yr4_financing", "yr4_depreciation", "yr4_fuel", "yr4_total", "yr5_tax_credit", "yr5_insurance",
                    "yr5_maintenance", "yr5_repairs", "yr5_taxs_fees", "yr5_financing", "yr5_depreciation", "yr5_fuel",
                    "yr5_total", "total_tax_credit", "total_insurance", "total_maintenance", "total_repairs",
                    "total_taxs_fees", "total_financing", "total_depreciation", "total_fuel", "total_total"]
    with open(output_file, 'w', newline='', encoding="utf8") as f_output:
        csv_output = csv.writer(f_output)

        csv_output.writerow(write_header)

    s = requests.Session()
    HEADER = {
        'newlic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwODYwNjUiLCJhcCI6IjQ1NTk0OTUyNSIsImlkIjoiMDllMzA3ZjRkYTc0OGFkOCIsInRyIjoiYWYzMWEyZmU2M2ZlMDZmYjAxMGM5MTRmMDM0MDM2MDAiLCJ0aSI6MTYyOTA3MzU2NDUzN319',
        'Referer': 'https://www.edmunds.com/tco.html',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'traceparent': '00-af31a2fe63fe06fb010c914f03403600-09e307f4da748ad8-01',
        'tracestate': '3086065@nr=0-1-3086065-455949525-09e307f4da748ad8----1629073564537',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36',
        'x-artifact-id': 'venom',
        'x-artifact-version': '2.0.622',
        'x-client-action-name': 'other_tco_index.makes',
        'x-deadline': '1629073565537',
        'x-edw-page-cat': 'other',
        'x-edw-page-name': 'other_tco_index',
        'x-referer': 'https://www.edmunds.com/tco.html',
        'x-trace-id': 'Root=1-6119f979-459601d63c13f1212e63b5e9',
        'x-trace-seq': '2'
    }
    headers = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Custom user agent',
        'My User Agent 1.0',
        'FutureSea Agent 1.0'
    ]

    HEADER1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    zipcode_url = "https://www.edmunds.com/v/api/location/zip/" + str(zipcode) + "/"
    r = s.get(zipcode_url, headers=HEADER)
    if r.status_code == 200:
        vehicle_type_url = "https://www.edmunds.com/gateway/api/vehicle/v4/makes/"
        vehicles = s.get(vehicle_type_url, headers=HEADER)
        result = vehicles.json()
        vehicle_types = result["results"].keys()
        for v_type in vehicle_types:
            payload = {
                'makeNiceId': str(v_type),
                'publicationStates': 'USED,NEW_USED,NEW',
                'distinct': 'year'}
            year_url = "https://www.edmunds.com/gateway/api/vehicle/v3/modelYears"
            get_years = s.get(year_url, params=payload, headers=HEADER)
            years = get_years.json()

            for year in years:
                if 2014 < int(year) < 2021:
                    model_load = {
                        'makeNiceId': str(v_type),
                        'year': int(year),
                        'fields': 'name,niceId,modelNiceId,publicationStates',
                        'sortby': 'name',
                        'pagesize': 1000,
                        'pagenum': 1
                    }
                    model_url = "https://www.edmunds.com/gateway/api/vehicle/v3/submodels"
                    get_models = s.get(model_url, params=model_load, headers=HEADER)
                    model_types = get_models.json()
                    models = model_types["results"]
                    for model in models:
                        style_load = {
                            'fields': 'id,name,niceName,niceId,trim(name),price'
                        }
                        style_url = "https://www.edmunds.com/gateway/api/vehicle/v4/makes/" + str(v_type) + "/models/" + \
                                    model[
                                        "modelNiceId"] + "/submodels/" + model["niceId"] + "/years/" + str(
                            year) + "/styles"

                        get_styles = s.get(style_url, params=style_load, headers=HEADER)
                        styles = get_styles.json()
                        last_results = styles["results"]
                        for result in last_results:
                            result_list = [str(year), str(v_type), model["modelNiceId"], str(result["id"])]

                            product_url = "https://www.edmunds.com/" + str(v_type) + "/" + str(
                                model["modelNiceId"]) + "/" + str(year) + "/cost-to-own/?style=" + str(
                                result["id"]) + "&zip=80202"
                            print(product_url)
                            try:
                                driver = webdriver.Chrome(options=co)
                                driver.delete_all_cookies()
                                driver.get(product_url)
                                htmlstring = driver.page_source
                                driver.close()
                                m_list = makelist(htmlstring)
                                result_list = result_list + m_list
                                with open(output_file, 'a', newline='', encoding="utf8") as f_output:
                                    csv_output = csv.writer(f_output)

                                    csv_output.writerow(result_list)
                            except:
                                miss_list.append(product_url)
                                time.sleep(5)
                                pass

                else:
                    pass

        print("done!")
    else:
        print("get error zipcode")



if __name__ == "__main__":
    main()
