import time


def test_search_example(selenium):

    # Open google search page:
    selenium.get('https://google.com')

    time.sleep(2)  # just for demo purposes, do NOT repeat it on real projects!

    # Find the field for search text input:
    search_input = selenium.find_element_by_name('q')

    # Enter the text for search:
    search_input.clear()
    search_input.send_keys('first test')

    time.sleep(2)  # just for demo purposes, do NOT repeat it on real projects!

    # Click Search:
    search_button = selenium.find_element_by_name("btnK")
    search_button.click()

    time.sleep(2)  # just for demo purposes, do NOT repeat it on real projects!

    # Make the screenshot of browser window:
    selenium.save_screenshot('result.png')

#     python -m pytest -v --driver Chrome --driver-path F:/обучение/Python/projects/chromedriver.exe test_selenium_simple.py