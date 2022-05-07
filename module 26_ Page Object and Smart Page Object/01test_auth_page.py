from pages.auth_page import AuthPage
import time


def test_auth_page(selenium):
    page = AuthPage(selenium)
    page.enter_email("email@gmail.com")
    page.enter_pass("pass")
    page.btn_click()

    # знак != или == будет зависеть от того, верные или неверные данные мы вводим
    assert page.get_relative_link() == '/all_pets', "login error"

    time.sleep(5)  # задержка для учебных целей

# python -m pytest -v --driver Chrome --driver-path F:/обучение/Python/projects/chromedriver.exe test_auth_page.py