import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# - task 25.3

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('F:/обучение/Python/projects/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    # Устанавливаем размер окна
    pytest.driver.set_window_size(1280, 1024)
    # Ставим неявное ожидание
    pytest.driver.implicitly_wait(5)
    yield

    pytest.driver.quit()


@pytest.fixture()
def test_login():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"


def test_show_all_pets(test_login):
    # Ставим неявное ожидание
    pytest.driver.implicitly_wait(5)

    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ',' in descriptions[i].text
        parts = descriptions[i].text.split(',')
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# - task 25.3.1, 25.5.1

def test_show_my_pets(test_login):
    # Нажимаем на кнопку мои питомцы
    pytest.driver.find_element_by_css_selector('a[href="/my_pets"]').click()
    # Проверяем, что оказались на странице мои питомцы
    assert pytest.driver.find_element_by_tag_name('h2').text == "vasya"

    # Ставим явное ожидание
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'all_my_pets')))

    # Ищем количество питомцев в статистике профиля
    my_pets = int((pytest.driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]').text.split())[2])
    # Ищем питомцев в профиле
    table_pets = pytest.driver.find_elements_by_xpath('//tbody/tr')
    # Ищем питомцев без фото
    no_images = pytest.driver.find_elements_by_xpath('//tbody/tr/th/img[@src=""]')
    # Ищем только имя питомцев в профиле
    names_0 = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    # Ищем только породу питомцев в профиле
    names_1 = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')
    # Ищем только возраст питомцев в профиле
    names_2 = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')

    # Сравниваем количество питомцев в статистике и в профиле
    assert my_pets == len(table_pets), 'Количество питомцев в статистике и в профиле не совпадают'
    # Проверяем, что хотя бы у половины питомцев есть фото
    assert my_pets // 2 >= len(no_images), 'У питомцев в профиле отсутствуют более 50% фото'

    # Проверяем, что у всех питомцев есть имя, возраст, порода
    for i in range(my_pets):
        assert names_0[i].text != '', 'В поле имя питомца есть пустое значение'
        assert names_1[i].text != '', 'В поле порода питомца есть пустое значение'
        assert names_2[i].text != '', 'В поле возраст питомца есть пустое значение'

    # Проверяем, что у всех питомцев разные имена
    try_names_0 = []
    for i in range(len(names_0)):
        if names_0[i].text == names_0[i].text:
            try_names_0 += names_0[i].text.split()
    assert my_pets == len(set(try_names_0)), 'Есть повторяющиеся имена у питомцев'

    # Проверяем, что в списке нет повторяющихся питомцев
    try_names_1 = []
    try_names_2 = []
    for i in range(len(names_0)):
        if names_1[i].text == names_1[i].text:
            try_names_1 += names_1[i].text.split()
        if names_2[i].text == names_2[i].text:
            try_names_2 += names_2[i].text.split()
    try_pets = [','.join(x) for x in zip(try_names_0, try_names_1, try_names_2)]
    assert my_pets == len(set(try_pets)), 'Есть повторяющиеся питомцы в списке'

# python -m pytest -v --driver Chrome --driver-path F:/обучение/Python/projects/chromedriver.exe test_selenium_petfriends.py