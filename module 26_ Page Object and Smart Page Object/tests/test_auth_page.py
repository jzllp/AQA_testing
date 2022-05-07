import pytest
from pages.auth_page import AuthPage

def test_authorisation(web_browser):

    page = AuthPage(web_browser)

    page.email.send_keys('test123@yandex.ru')

    page.password.send_keys("123456")

    page.btn.click()

    assert page.get_current_url() == 'http://petfriends1.herokuapp.com/all_pets'


# python -m pytest -v --driver Chrome --driver-path F:/обучение/Python/projects/chromedriver.exe tests/test_auth_page.py