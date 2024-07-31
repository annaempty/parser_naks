from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re


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


def enter_date(browser, date_from, date_to):
    """
    Находит поля с датами и заполняет их
    :param browser: веб-сайт
    :param date_from: дата от
    :param date_to: дата до
    :return:
    """
    # id поля ввода "даты от" - arrFilter_DATE_ACTIVE_TO_1
    elem_data_1 = browser.find_element(By.ID, 'arrFilter_DATE_ACTIVE_TO_1')
    elem_data_1.send_keys(date_from + Keys.RETURN)
    # id поля ввода "даты по" -arrFilter_DATE_ACTIVE_TO_2
    time.sleep(1)
    elem_data_2 = browser.find_element(By.ID, 'arrFilter_DATE_ACTIVE_TO_2')
    elem_data_2.send_keys(date_to + Keys.RETURN)
    time.sleep(1)
    return browser


def find_button_to_switch(browser):
    """
    Находит кнопку "Следующая"
    :param browser: веб-сайт
    :return: кнопка "След", None - если дошли до конца
    """
    try:
        btn = browser.find_element(By.XPATH, "//a[text()='След.']")
        return btn
    except NoSuchElementException:
        print('Button \'Следующая\' not found')
        return None


def check_number_entries(elem):
    """
    Проверяет вышли ли мы за пределы ограничения на вывод
    нужно переписать с использованием библиотеки selenium
    1. Найти элемент
    2. выудить количество записей
    3. Выкинуть предупреждение если необходимо

    :param elem:
    :return: ничего
    """
    number_pattern = r"\d{1,3}"
    find_pattern = r"НАЙДЕНО ЗАПИСЕЙ"
    if not re.search(find_pattern, elem[0].text) is None:
        if int(re.search(number_pattern, elem[0].text)) == 500:
            print("Скорее всего превышен лимит по количеству записей (500 или больше)")


def switch_webpage(browser, btn):
    """
    Переключает страницу через кнопку "Следующая"
    :param browser: веб-сайт, btn - кнопка "Следующая"
    :return: browser: веб-сайт (возможно не нужно)
    """
    if btn:
        ActionChains(browser).move_to_element(btn).click().perform()
        time.sleep(1)
    return browser


if __name__ == '__main__':
    html = 'https://naks.ru/registry/reg/st/?PAGEN_1=1&arrSORT=&arrFilter_pf%5Bnum_acst%5D%5B%5D=3173145&arrFilter_pf%5Bnum_sv%5D=%C0%D6%D1%D2-87-&arrFilter_DATE_ACTIVE_TO_1=01.01.2027&arrFilter_DATE_ACTIVE_TO_2=31.12.2027&arrFilter_ff%5BNAME%5D=&arrFilter_ff%5BPREVIEW_TEXT%5D=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
    browser = open_web(html)
    while True:
        btn = find_button_to_switch(browser)
        if btn:
            browser = switch_webpage(browser, btn)
        else:
            break

