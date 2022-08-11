import pytest
from selenium import webdriver



@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('/Users/Andrew Shabailov/PycharmProjects/Task_25.5.1/tests/chromedriver')
   pytest.driver.implicitly_wait(10)
   # Перейти на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   # Ввести email
   pytest.driver.find_element_by_id('email').send_keys('kuku@tut.by')
   # Ввести пароль
   pytest.driver.find_element_by_id('pass').send_keys('123')
   # Нажать на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

   yield

   pytest.driver.quit()