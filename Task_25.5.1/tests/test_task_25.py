from collections import Counter

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytest

from selenium.webdriver.common.by import By


def test_show_my_pets():
   # Проверить, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
   # Зайти на страницу "Мои питомцы"
   pytest.driver.find_element_by_xpath("//a[@class='nav-link']").click()
   # Проверить, что мы на странице "Мои питомцы"
   assert pytest.driver.find_element_by_tag_name('h2').text == "Andrew Sha"

def test_check_my_pets():
   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
   # Проверить, что на странице "Мои питомцы" присутствуют все питомцы
   # Из всей таблицы питомцев
   pets_list = pytest.driver.find_element_by_xpath("//tbody")
   # Выбрать список питомцев из этой таблицы, каждый из элементов лежит в тегах 'tr'
   pets_list_info = pets_list.find_elements_by_tag_name('tr')
   # Добываем число, находящееся в блоке слева напротив слова "Питомцев: "
   number_of_pets = pytest.driver.find_element(By.XPATH, "(//div[@class='.col-sm-4 left'])[1]").text.replace("\n", "").split(": ")[1].split("Друзей")[0]
   # Убеждаемся, что мы добыли его верно
   print(number_of_pets)
   # Сравниваем длину списка питомцев из таблицы с числом из блока слева
   assert len(pets_list_info) == int(number_of_pets)

def test_pets_list_have_photo():
   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
   # Проверить, что на странице "Мои питомцы" присутствуют все питомцы
   # Из всей таблицы питомцев
   pets_list = pytest.driver.find_element_by_xpath("//tbody")
   # Проверить список питомцев по тегу img
   pets_list_photo = pets_list.find_elements_by_tag_name('img')
   # Посчитать кол-во тех питомцев, у которых значение абрибута scr в теге img не равно нулю, то есть есть ссылка на фото
   counter = 0
   for i in pets_list_photo:
      if i.get_attribute('src') != "":
         counter += 1
   # Проверить, что питомцев с фото больше либо равно половине всего списка питомцев с тегом img
   assert counter >= len(pets_list_photo) / 2, 'The page have NO pet`s photos'

def test_pets_info_not_null():
   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
   # Проверить, что на странице "Мои питомцы" присутствуют все питомцы
   # Из всей таблицы питомцев
   pets_list = pytest.driver.find_element_by_xpath("//tbody")
   # Новый список питомцев
   each_pet = pets_list.find_elements_by_tag_name('tr')
   # Создать пустой список, куда будем помещать добытый циклом список элементов "Кличка", "Порода", "Возраст" для каждого питомца вперемешку
   pets_list_info = []
   for i in each_pet:
      pets_list_info.append(list(i.find_elements_by_tag_name('td')))
   # Циклом получившийся список разбить на отдельные элементы "Кличка", "Порода", "Возраст"
   bad_pet = False

   for i in pets_list_info:
      pet_name = i[0].text
      pet_breed = i[1].text
      pet_age = i[2].text
   # Если какой-то из этих элементов пуст, то прервать цикл
      if pet_name == "" or pet_breed == "" or pet_age == "":
         bad_pet = True
         break

   assert bad_pet == False

def test_only_unique_pet_names():
   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
   # Проверить, что на странице "Мои питомцы" присутствуют все питомцы
   pets_list = pytest.driver.find_element_by_xpath("//tbody")
   each_pet = pets_list.find_elements_by_tag_name('tr')
   # Создать пустой список питомцев, куда с помощью цикла будем класть имена питомцев
   pet_names = []

   for i in each_pet:
      pet_names.append(i.find_element_by_tag_name('td').text)


   assert len(Counter(pet_names)) == len(each_pet)

def test_only_unique_pet_data():
   pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
   WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody")))
   # Проверить, что на странице "Мои питомцы" присутствуют все питомцы
   pets_list = pytest.driver.find_element_by_xpath("//tbody")
   each_pet = pets_list.find_elements_by_tag_name('tr')

   pets_list_info = []
   for i in each_pet:
      separated_pets_attribute = i.find_elements_by_tag_name('td')
      name = separated_pets_attribute[0].text
      age = separated_pets_attribute[1].text
      breed = separated_pets_attribute[2].text

      pets_list_info.append(name+age+breed)

   print(Counter(pets_list_info))

   assert len(Counter(pets_list_info)) == len(pets_list_info)

# для запуска теста "pytest -s -v test_task_25.py" из дирректории с файлом теста