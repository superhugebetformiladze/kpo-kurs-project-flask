from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def wait_find(locator, value, browser):
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((locator, value))
    )

def wait_clear(locator, value, browser):
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((locator, value))
    ).clear()

def wait_click(locator, value, browser):
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((locator, value))
    ).click()

def wait_send_keys(locator, value, browser, keys):
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((locator, value))
    ).send_keys(keys)

def login(browser, login, password):
    wait_click(By.LINK_TEXT, 'Вход', browser)
    wait_send_keys(By.ID, 'login', browser, login)
    wait_send_keys(By.ID, 'password', browser, password)
    wait_click(By.XPATH, '//*[@id="login-form"]/input', browser)

def add_service(browser, name, description, additional_info, price):
    wait_click(By.ID, 'products', browser)
    wait_click(By.LINK_TEXT, 'Добавить', browser)
    wait_send_keys(By.NAME, 'service_name', browser, name)
    wait_send_keys(By.NAME, 'description', browser, description)
    wait_send_keys(By.NAME, 'additional_info', browser, additional_info)
    wait_send_keys(By.NAME, 'price', browser, price)
    wait_click(By.XPATH, '/html/body/div[2]/div/div[2]/form/button', browser)

def edit_service(browser, name, description, additional_info, price):
    wait_click(By.ID, 'products', browser)
    wait_click(By.XPATH, '/html/body/div[2]/main/section[2]/table/tbody/tr[11]/td[7]/div/a[1]', browser)
    wait_clear(By.NAME, 'service_name', browser)
    wait_send_keys(By.NAME, 'service_name', browser, name)
    wait_clear(By.NAME, 'description', browser)
    wait_send_keys(By.NAME, 'description', browser, description)
    wait_clear(By.NAME, 'additional_info', browser)
    wait_send_keys(By.NAME, 'additional_info', browser, additional_info)
    wait_clear(By.NAME, 'price', browser)
    wait_send_keys(By.NAME, 'price', browser, price)
    wait_click(By.XPATH, '/html/body/div[2]/div/div[2]/form/button', browser)

def delete_service(browser):
    wait_click(By.ID, 'products', browser)
    wait_click(By.XPATH, '/html/body/div[2]/main/section[2]/table/tbody/tr[11]/td[7]/div/a[2]', browser)


def check_service(browser, expected_name, expected_description, expected_additional_info, expected_price):
    wait_click(By.ID, 'products', browser)

    name = browser.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/table/tbody/tr[11]/td[2]')
    description = browser.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/table/tbody/tr[11]/td[3]')
    additional_info = browser.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/table/tbody/tr[11]/td[4]')
    price = browser.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/table/tbody/tr[11]/td[5]')

    
    assert name.text == expected_name
    assert description.text == expected_description
    assert additional_info.text == expected_additional_info
    assert price.text == expected_price


def check_deleted_service(browser):
    wait_click(By.ID, 'products', browser)

    try:
        browser.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/table/tbody/tr[11]/td[2]')

        raise AssertionError("Услуга не была удалена")
    except NoSuchElementException:
        return True
    

def tests():
    browser = webdriver.Chrome()
    browser.get('http://127.0.0.1:5000/')

    login(browser, 'admin', 'admin1234')

    wait_click(By.LINK_TEXT, 'Админ Панель', browser)
    add_service(browser, 'Название услуги', 'Описание', 'Доп информация', '1234')
    check_service(browser, 'Название услуги', 'Описание', 'Доп информация', '1234')
    edit_service(browser, 'Название услуги измененное', 'Описание измененное', 'Доп информация измененное', '12345')
    check_service(browser, 'Название услуги измененное', 'Описание измененное', 'Доп информация измененное', '12345')
    delete_service(browser)
    check_deleted_service(browser)


    browser.quit()


if __name__ == '__main__':
    tests()
