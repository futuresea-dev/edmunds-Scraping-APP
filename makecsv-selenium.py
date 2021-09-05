# utf-8
import time
import requests
import csv
from bs4 import BeautifulSoup
import random
import undetected_chromedriver as webdriver
import json

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
co.add_argument("--referer=https://www.edmunds.com/tco.html")
co.add_argument('--disable-blink-features=AutomationControlled')
def get_proxies():
    with open("proxy.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    PROXIES = [x.strip() for x in content]

    return PROXIES


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
        totals = soup.find('div', attrs={'class': 'pricing-section mb-1_5 mb-md-0 row'})
        t_cash = totals.findAll('p', attrs={'class': 'pricing-value heading-2 mb-0'})
        com.append(t_cash[1].contents[0])
    except:
        pass

    return com


# Create a request interceptor
def interceptor(request):
    del request.headers['Referer']  # Delete the header first
    request.headers['Referer'] = 'https://www.edmunds.com/tco.html'


def main():
    PROXIES = get_proxies()
    missList = []
    zipcode = "80202"
    output_file = str(zipcode) + "_last_output.csv"
    write_header = ["vehicle_year", "vehicle_make", "vehicle_model", "vehicle_style", "total_cash_price",
                    "yr1_tax_credit", "yr1_insurance",
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
        'Referer': 'https://www.edmunds.com/tco.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36'
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
                        style_list = []
                        for result in last_results:
                            style_list.append(result["id"])
                        style_string = ','.join(str(e) for e in style_list)
                        # pxy = random.choice(PROXIES)
                        # proxyDict = {
                        #     "http": pxy,
                        #     "https": pxy,
                        #     "ftp": pxy
                        # }

                        product_url = "https://www.edmunds.com/gateway/api/tco/v3?zip=80202&styleIds=" + style_string
                        try:
                            # content = requests.get(product_url, headers=HEADER, timeout=5)
                            driver = webdriver.Chrome(options=co)

                            driver.get(product_url)
                            try:
                                content = driver.find_element_by_tag_name("body").text
                                htmlstring = json.loads(content)
                                tco_result = htmlstring["results"]
                                for result in last_results:
                                    result_list = [str(year), str(v_type), model["modelNiceId"], str(result["name"])]
                                    vec_id = str(result["id"])
                                    if tco_result[vec_id] != {}:
                                        result_list.append('${:,.2f}'.format(tco_result[vec_id]["totalCash"]))
                                        years_list = tco_result[vec_id]["years"]
                                        total_list = tco_result[vec_id]["total"]
                                        for key, yea in years_list.items():
                                            result_list.append('${:,.2f}'.format(0))
                                            for key1, value in yea.items():
                                                if key1 != 'averageCostPerMile':
                                                    result_list.append('${:,.2f}'.format(value))
                                        for key1, value in total_list.items():
                                            if key1 != 'averageCostPerMile':
                                                result_list.append('${:,.2f}'.format(value))
                                        with open(output_file, 'a', newline='', encoding="utf8") as f_output:
                                            csv_output = csv.writer(f_output)
                                            csv_output.writerow(result_list)
                                    else:
                                        with open(output_file, 'a', newline='', encoding="utf8") as f_output:
                                            csv_output = csv.writer(f_output)
                                            csv_output.writerow(result_list)

                            except:
                                print(product_url + " error")
                                pass
                            driver.close()
                        except:
                            missList.append(product_url)
                            print(missList)
                            pass
                else:
                    pass

        print("done!")
    else:
        print("get error zipcode")


if __name__ == "__main__":
    main()
