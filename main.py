import pytest
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_pets(browser):
    """
    Тестовый сценарий для проверки списка питомцев на сайте.

   """
    results = []

    # Авторизация на сайте
    browser.get("https://petfriends.skillfactory.ru/login")
    browser.find_element(By.ID, "email").send_keys('email')
    browser.find_element(By.ID, "pass").send_keys('password')
    browser.find_element(By.CSS_SELECTOR,"body > div > div > form > div.text-center > button").click()

    # Переход на страницу со списком питомцев
    browser.get("https://petfriends.skillfactory.ru/my_pets")

    # Ожидание загрузки таблицы питомцев
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#all_my_pets > table")))

    # Получение информации о каждом питомце из таблицы
    rows = browser.find_elements(By.CSS_SELECTOR, "#all_my_pets > table > tbody > tr")
    pets_details = []
    photos_count = 0
    for row in rows:
        photo = WebDriverWait(row, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "th > img"))).get_attribute("src")
        name = WebDriverWait(row, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(2)"))).text
        breed = WebDriverWait(row, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(3)"))).text
        age = WebDriverWait(row, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td:nth-child(4)"))).text

        if photo:
            photos_count += 1
        pets_details.append((name, breed, age))

    # Формирование результатов проверок
    results.append(f"Присутствуют {len(pets_details)} питомцев.")
    results.append(f"Из {len(rows)} питомцев, {photos_count} имеют фото.")
    for name, breed, age in pets_details:
        results.append(f"Имя питомца: {name}, Возраст: {age}, Порода: {breed}")

    if len(pets_details) == len(set(pets_details)):
        results.append("Все питомцы имеют уникальные комбинации имени, породы и возраста.")
    else:
        results.append("Некоторые питомцы имеют одинаковые комбинации имени, породы и возраста.")

    duplicates = [item for item, count in Counter(pets_details).items() if count > 1]
    if not duplicates:
        results.append("В списке нет повторяющихся питомцев.")
    else:
        results.append(f"В списке есть следующие повторяющиеся питомцы: {', '.join([dup[0] for dup in duplicates])}")

    # Вывод результатов проверок
    for result in results:
        print(result)