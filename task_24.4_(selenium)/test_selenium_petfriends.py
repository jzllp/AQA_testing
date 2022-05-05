import pickle
import time


def test_petfriends(selenium):

    # Open PetFriends base page:
    selenium.get("https://petfriends1.herokuapp.com/")

    time.sleep(2)  # just for demo purposes, do NOT repeat it on real projects!

    # Find the field for search text input:
    btn_newuser = selenium.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")

    btn_newuser.click()

    btn_exist_acc = selenium.find_element_by_link_text(u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    field_email = selenium.find_element_by_id("email")
    field_email.click()
    field_email.clear()
    field_email.send_keys("vasya@mail.com")

    field_pass = selenium.find_element_by_id("pass")
    field_pass.click()
    field_pass.clear()
    field_pass.send_keys("12345")

    btn_submit = selenium.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    # Save cookies of the browser after the login
    with open('my_cookies.txt', 'wb') as cookies:
        pickle.dump(selenium.get_cookies(), cookies)

    # Make the screenshot of browser window:
    selenium.save_screenshot('result_petfriends.png')

#     python -m pytest -v --driver Chrome --driver-path F:/обучение/Python/projects/chromedriver.exe test_selenium_petfriends.py

