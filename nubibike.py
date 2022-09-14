from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re


import requests
from bs4 import BeautifulSoup


def nubiBike(result):
    url = 'https://www.nubija.com/terminal/terminalList.do'

    response = requests.get(url)
    result = []

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select_one('#terminal_list > table')
        # print(table)
        location = table.find_all('tr')
        for elem in location:
            try:
                img = str(elem.select_one('img'))
                num_find = re.findall(r'\d+', img)
                num = int(num_find[0])
                name = elem.find(
                    'td', class_='list_terminal_name').get_text().strip()
                location = elem.find(
                    'td', class_='list_terminal_location').get_text()
                # print(name)
                # print(location)
                result.append([num] + [name] + [location])
            except Exception as e:
                continue

    else:
        print(response.status_code)

    print(result)
    return result


def main():
    result = []
    result = nubiBike(result)
    nubi_tbl = pd.DataFrame(result, columns=(
        'num', 'name', 'location'))
    nubi_tbl.to_csv('nubibike.csv',
                    encoding='cp949', mode='w', index=True)


if __name__ == '__main__':
    main()