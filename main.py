from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
from select_date import enter_date, open_web, switch_webpage, find_button_to_switch



def find_table_body(browser):
    """
    Принимает: browser - html браузер
    Функция принимает уже открытый по необходимой ссылке сайт
    и находит список элементов tr в таблице с необходимыми нам данными.
    Возвращает список из веб-элементов
    """

    table = browser.find_element(By.XPATH, "//table[@class='tabl']")
    #tbody = table.find('tbody')
    tbody_r = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
    return tbody_r


def read_title(tbody_r, num_of_skip_col):
    """
    Функция считывает первую строку таблицы (заголовки)
    :param tbody_r: список веб-элементов
    :return: dict_colum: словарь с названиями колонок
    """
    dict_colum = {}
    tbody_d = tbody_r[0].find_elements(By.TAG_NAME, 'td')
    for j in range(len(tbody_d) - num_of_skip_col):
        dict_colum[j] = tbody_d[j].text.strip()
    return dict_colum


def read_data(tbody_r, num_of_skip_col, dict_tail):
    """
    Функция считывает основную часть таблицы (тело) на текущей странице
    :param tbody_r: список веб-элементов
    :return: dict_tail: словарь с основной частью таблицы
    """
    for i in range(1, len(tbody_r)):
        tbody_d = tbody_r[i].find_elements(By.TAG_NAME, 'td')
        for j in range(len(tbody_d) - num_of_skip_col):
            if j not in dict_tail:
                dict_tail[j] = []
            dict_tail[j].append(tbody_d[j].text.strip())
    return dict_tail


if __name__ == '__main__':
    # Необходимо будет вынести в текстовый файл:
    html = 'https://naks.ru/registry/reg/st/?arrSORT=&arrFilter_pf%5Bnum_acst%5D%5B%5D=3173145&arrFilter_pf%5Bnum_sv%5D=%C0%D6%D1%D2-87-&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_ff%5BNAME%5D=&arrFilter_ff%5BPREVIEW_TEXT%5D=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
    date_from = '01.01.2024'
    date_to = '31.12.2024'
    num_of_skip_col = 2  # Количество пропускаемых(неинформативных) столбцов с конца

    browser = open_web(html)
    browser = enter_date(browser, date_from, date_to)

    dict = {}
    start_table = find_table_body(browser)
    dict_columns = read_title(start_table, num_of_skip_col)
    dict = read_data(start_table, num_of_skip_col, dict)
    while True:
        btn = find_button_to_switch(browser)
        if btn:
            browser = switch_webpage(browser, btn)
            start_table = find_table_body(browser)
            dict = read_data(start_table, num_of_skip_col, dict)
        else:
            break
    df = pd.DataFrame(dict)
    df.rename(columns=dict_columns, inplace=True)
    print(df)
    #df.to_csv('naks.csv', sep=';')


    #df_read = pd.read_csv('naks.csv', sep=';')
    #df.append(df_1)
    #elements = browser.find_element(By.CLASS_NAME, 'zagolovok-tabl')
    #class ="col-md-8 col-xl-9 order-2 order-md-1"



