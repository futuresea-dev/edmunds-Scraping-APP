import json
import requests
import csv
from bs4 import BeautifulSoup

def get_leaves(item, key=None):
    if isinstance(item, dict):
        leaves = []
        for i in item.keys():
            leaves.extend(get_leaves(item[i], i))
        return leaves
    elif isinstance(item, list):
        leaves = []
        for i in item:
            leaves.extend(get_leaves(i, key))
        return leaves
    else:
        return [(key, item)]


def main():
    zipcode = input("Please Input zipcode : ")
    output_file = str(zipcode) + "_output.csv"
    s = requests.Session()
    # zipcode = "80202"
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

    write_header = True
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
                if int(year) < 2015:
                    pass
                else:
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
                                        "modelNiceId"] + "/submodels/" + model["niceId"] + "/years/" + str(year) + "/styles"
                        get_styles = s.get(style_url, params=style_load, headers=HEADER)
                        styles = get_styles.json()
                        last_results = styles["results"]
                        with open(output_file, 'a', newline='', encoding="utf8") as f_output:
                            for result in last_results:
                                csv_output = csv.writer(f_output)

                                leaf_entries = sorted(get_leaves(result))

                                if write_header:
                                    csv_output.writerow([k for k, v in leaf_entries])
                                    write_header = False

                                csv_output.writerow([v for k, v in leaf_entries])
                        # product_url = "https://www.edmunds.com/" + str(v_type) + "/" + model["modelNiceId"] +"/" + str(year) +"/cost-to-own/"
                        # products_content = s.get(product_url, headers=HEADER)
                        # print(products_content.content)
        print("done!")
    else:
        print("get error zipcode")


if __name__ == "__main__":
    main()
