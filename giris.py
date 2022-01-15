from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from time import sleep
import undetected_chromedriver as uc
browser = uc.Chrome()

browser.get("https://instagram.com")
sleep(2)
giris = browser.find_element_by_name("username")
giris.send_keys("denemescrapysayko")
sleep(3)
sifre = browser.find_element_by_name("password")
sifre.send_keys("sayko119")
sifre.send_keys(Keys.RETURN)
sleep(5)

file = open("userlist.txt","r")
for username in file:
    browser.get("https://instagram.com/"+username)
    sleep(2)
    followButton =browser.find_element_by_xpath("//*[text()='Follow']")
    followButton.click()
sleep(2600)