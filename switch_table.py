from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from select_date import open_web

import time


def switch_table(browser):
    try:
        element = browser.find_element(By.XPATH, "//a[text()='След.']")
        ActionChains(browser).click(element).perform()
        ref = browser.find_element(By.XPATH, "//a[@class='text']")
        print(ref.text)
        time.sleep(4)
        return browser
    except:
        return None



if __name__ == "__main__":
    html = 'https://naks.ru/registry/reg/st/?arrSORT=&arrFilter_pf%5Bnum_acst%5D%5B%5D=3173145&arrFilter_pf%5Bnum_sv%5D=%C0%D6%D1%D2-87-&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_ff%5BNAME%5D=&arrFilter_ff%5BPREVIEW_TEXT%5D=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
    browser = open_web(html)
    for i in range(2, 11):
        element = browser.find_element(By.XPATH, f"//a[text()='{str(i)}']")
        ActionChains(browser).move_to_element(element).click().perform()
        print(browser.find_element(By.XPATH, "//table[@class='tabl']").text)
        time.sleep(4)
    time.sleep(4)

