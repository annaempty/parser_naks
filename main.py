from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
from select_date import find_table_by_date, open_web, switch_webpage



def find_table_body(html_text):
    # Переписать поиск таблицы как тут -> ref = browser.find_element(By.XPATH, "//a[text()='След.']")
    root = BeautifulSoup(html_text, 'html.parser')
    field = root.find('div', {"class": "col-md-8 col-xl-9 order-2 order-md-1"})
    table = field.find('table', {'class': 'tabl'})
    tbody = table.find('tbody')
    tbody_r = tbody.find_all('tr')
    return tbody_r


def read_title(tbody_r):
    dict_colum = {}
    tbody_d = tbody_r[0].find_all('td')
    for j in range(len(tbody_d)):
        dict_colum[j] = tbody_d[j].text.strip()
    return dict_colum


def read_data(tbody_r):
    dict_tail = {}
    for i in range(1, len(tbody_r)):
        tbody_d = tbody_r[i].find_all('td')
        for j in range(len(tbody_d)-2):
            if j not in dict_tail:
                dict_tail[j] = []
            dict_tail[j].append(tbody_d[j].text.strip())
    df = pd.DataFrame(dict_tail)
    return df


if __name__ == '__main__':
    # Необходимо будет вынести в текстовый файл:
    html = 'https://naks.ru/registry/reg/st/?arrSORT=&arrFilter_pf%5Bnum_acst%5D%5B%5D=3173145&arrFilter_pf%5Bnum_sv%5D=%C0%D6%D1%D2-87-&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_ff%5BNAME%5D=&arrFilter_ff%5BPREVIEW_TEXT%5D=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
    date_from = '01.01.2024'
    date_to = '31.12.2024'

    browser = open_web(html)
    browser, html_text = find_table_by_date(browser, date_from, date_to)
    start_table = find_table_body(html_text)
    dict_columns = read_title(start_table)
    print(dict_columns)
    df = read_data(start_table)
    df.rename(columns=dict_columns)
    df.to_csv('naks.csv', sep=';')
    #df_read = pd.read_csv('naks.csv', sep=';')
    #df.append(df_1)
    #elements = browser.find_element(By.CLASS_NAME, 'zagolovok-tabl')
    #class ="col-md-8 col-xl-9 order-2 order-md-1"



