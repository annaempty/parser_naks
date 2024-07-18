from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re


# Открывет сайт по ссылке
def open_web(html):
    """
    Открывает сайт по ссылке (ссылка должна вести на сайт,
    где уже выбран аттестационный пункт)
    :param html: ссылка на сайт
    :return: browser: веб-сайт
    """
    option = Options()
    option.add_argument("--disable-infobars")
    browser = webdriver.Chrome(option)
    browser.get(html)
    return browser


# Находит поля с датами и заполняет их
def find_table_by_date(browser, date_from, date_to):
    """
    Заполняет поля с датами
    :param browser: веб-сайт
    :param date_from: дата от
    :param date_to: дата до
    :return:
    """
    # id первой кнопки аттестации до - arrFilter_DATE_ACTIVE_TO_1
    elem_data_1 = browser.find_element(By.ID, 'arrFilter_DATE_ACTIVE_TO_1')
    elem_data_1.send_keys(date_from + Keys.RETURN)

    # id второй кнопки аттестации до -arrFilter_DATE_ACTIVE_TO_2
    time.sleep(4)
    elem_data_1 = browser.find_element(By.ID, 'arrFilter_DATE_ACTIVE_TO_2')
    elem_data_1.send_keys(date_to + Keys.RETURN)
    time.sleep(4)
    # class кнопки фильтр inputbuttonflat
    # На кнопку фильтр тыкать не нужно, фильтруется после ввода дат
    # browser.find_element(By.CLASS_NAME, 'inputbuttonflat').click()
    # time.sleep(10)
    #html_text = browser.page_source
    return browser


def find_button_to_switch(browser):
    """
    Находит список кнопок для перехода на страничку с другими технологиями
    Тут нужно реализовать нажатие на клавишу и поиск кнопки через try
    :param browser: веб-сайт
    :return: пока ничего полезного
    """

    # через try: 
    ref = browser.find_element(By.XPATH, "//a[text()='След.']")
    new_window_url = "https://naks.ru" + ref.get_attribute("href") # я не уверена, что так работает
    print(ref.text)

    return browser, ref


def check_number_entries(elem):
    number_pattern = r"\d{1,3}"
    find_pattern = r"НАЙДЕНО ЗАПИСЕЙ"
    if not re.search(find_pattern, elem[0].text) is None:
        if int(re.search(number_pattern, elem[0].text)) == 500:
            print("Скорее всего превышен лимит по количеству записей (500 или больше)")


def switch_webpage(browser, list_elem):
    # Нажать на кнопку следующее, но уже не работает, если когда-то работала 
    switch_1_step = list_elem[1].find_element(By.CLASS_NAME, 'text')
    switch_buttons_list = switch_1_step[1].find_element(By.CSS_SELECTOR, 'a')
    for switch_button in switch_buttons_list:
        if switch_button.text == 'След.':
            login_button = switch_button
            new_window_url = login_button.get_attribute("href")
            browser.get(new_window_url)
            return browser


if __name__ == '__main__':
    html = 'https://naks.ru/registry/reg/st/?PAGEN_1=1&arrSORT=&arrFilter_pf%5Bnum_acst%5D%5B%5D=3173145&arrFilter_pf%5Bnum_sv%5D=%C0%D6%D1%D2-87-&arrFilter_DATE_ACTIVE_TO_1=01.01.2027&arrFilter_DATE_ACTIVE_TO_2=31.12.2027&arrFilter_ff%5BNAME%5D=&arrFilter_ff%5BPREVIEW_TEXT%5D=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
    browser = open_web(html)
    browser, list_elem = find_button_to_switch(browser)
    # browser, list_elem = switch_webpage(browser, list_elem)
