import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

balance_sheet_url = 'https://www.moneycontrol.com/financials/relianceindustries/consolidated-balance-sheetVI/'
quaterly_url = 'https://www.moneycontrol.com/financials/relianceindustries/profit-lossVI/'
cash_flow_url = 'https://www.moneycontrol.com/financials/relianceindustries/consolidated-cash-flowVI/'


def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table')
        #         if len(table)>1:
        cells = table[1].find_all('tr')[0].find_all('td')
        headers = [cell.get_text(strip=True) for cell in cells]
        rows = []
        for tr in table[1].find_all('tr')[1:]:  # Skip the header row
            cells = tr.find_all('td')
            row = [cell.get_text(strip=True) for cell in cells]
            rows.append(row)
        df = pd.DataFrame(rows, columns=headers)
        return (df)
    else:
        return (pd.DataFrame())


def get_all_data(url):
    data = pd.DataFrame()
    try:
        data = get_data(url + '1')
        for i in range(2, 30):
            n_data = get_data(url + str(i))
            data[n_data.columns[1:]] = n_data[n_data.columns[1:]]
            #
            print(
                "#" * 10,
                i,
            )
        return (data.set_index(data.columns[0]))
    except:
        #         print(f"pages ended at {i}")
        if len(data) != 0:
            return (data.set_index(data.columns[0]))


sym = ((pd.read_csv(
    'https://raw.githubusercontent.com/Shivrtn/stock_pred_model_helper/master/remaning_name_moneycontrol.csv'
)))
data_dic = {}
for i in range(0, 3):
    n = sym.iloc[i]['0']

    print(i, ' : ', n)
    try:
        # if ((data_dic[list(data_dic.keys())[i]][0].shape[1]) !=(data_dic[list(data_dic.keys())[i]][1].shape[1])!=(data_dic[list(data_dic.keys())[i]][2].shape[1])):
        data_1 = get_all_data(balance_sheet_url + n + "/")
        data_2 = get_all_data(quaterly_url + n + "/")
        data_3 = get_all_data(cash_flow_url + n + "/")
        if (data_1.shape[1] == data_2.shape[1] == data_3.shape[1]):

            data_dic[sym.iloc[i]['Unnamed: 0']] = [data_1, data_2, data_3]
        # else:
        #     print("equal")
    except:
        print("tried but not get")
        pass
np.save("data_dic_1.npy", data_dic)
