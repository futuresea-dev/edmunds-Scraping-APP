import requests
import csv
from bs4 import BeautifulSoup
import random

with open("miss.csv") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
miss_price_list = [x.strip() for x in content]
HEADER = {
    'Referer': 'https://www.edmunds.com/tco.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.131 Safari/537.36'
}

output_miss_file = "80202_last_output_miss.csv"
for miss_price_url in miss_price_list:

    content = requests.get(miss_price_url, headers=HEADER, timeout=15)
    if content.status_code == 200:
        last_results = miss_price_url.replace("https://www.edmunds.com/gateway/api/tco/v3?zip=80202&styleIds=", "").split(",")
        htmlstring = content.json()
        tco_result = htmlstring["results"]
        for result in last_results:
            result_list = [str(result)]
            vec_id = str(result)
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
                with open(output_miss_file, 'a', newline='', encoding="utf8") as f_output:
                    csv_output = csv.writer(f_output)
                    csv_output.writerow(result_list)
            else:
                with open(output_miss_file, 'a', newline='', encoding="utf8") as f_output:
                    csv_output = csv.writer(f_output)
                    csv_output.writerow(result_list)