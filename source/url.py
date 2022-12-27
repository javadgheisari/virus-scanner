from selenium import webdriver
from time import sleep

driver = webdriver.Firefox()
url = ''
while True:
    url_old = url
    url = driver.current_url
    if url != 'about:blank' and url_old != url:
        print(url)
    sleep(3)