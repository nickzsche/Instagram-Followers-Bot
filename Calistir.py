import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from NickzscheBot import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QShortcut, QFileDialog
from selenium import webdriver
import time
import os
from selenium.webdriver.common.keys import Keys
import threading
import sqlite3
from selenium.webdriver.support.ui import Select
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMessageBox
import webbrowser
import undetected_chromedriver as uc


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(self.Login)
        self.ui.pushButton.clicked.connect(self.TakipciCek)
        self.ui.pushButton_2.clicked.connect(self.TakipEt)
        self.ui.pushButton_5.clicked.connect(self.HintButton)

    def Login(self):
        giris = self.ui.lineEdit.text()
        sifre = self.ui.lineEdit_2.text()

    def TakipciCek(self):
        def TakipciCekThread():
            browser = webdriver.Chrome("chromedriver.exe")
            browser.get("https://www.instagram.com")
            user = self.ui.lineEdit.text()
            password = self.ui.lineEdit_2.text()
            time.sleep(2)
            browser.find_element_by_name("username").send_keys(user)
            browser.find_element_by_name("password").send_keys(password)
            browser.find_element_by_xpath(
                "//*[@id='loginForm']/div/div[3]/button/div").click()
            time.sleep(5)
            links = self.ui.lineEdit_3.text()
            linkSplit = links.split(",")
            for link in linkSplit:
                browser.get(f"https://www.instagram.com/{link}")
                time.sleep(2)
                followersList = browser.find_element_by_xpath(
                    "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
                followersList.click()
                time.sleep(2)
                print(link)
                dialog = browser.find_element_by_css_selector(
                    "div[role=dialog] ul")
                followerCount = len(dialog.find_elements_by_css_selector("li"))
                action = webdriver.ActionChains(browser)

                while True:
                    dialog.click()
                    action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
                    time.sleep(2)
                    newCount = len(dialog.find_elements_by_css_selector("li"))

                    if followerCount < 250:
                        followerCount = newCount
                        print(f"Güncel liste {newCount}")
                        time.sleep(3)
                        pass
                    else:
                        break
                followers = dialog.find_elements_by_css_selector("li")
                for user in followers:
                    link = user.find_element_by_css_selector(
                        "a").get_attribute("href")
                    followerListTxt = open("FollowersList.txt", "a")
                    followerListTxt.write(link+"\n")
                    print(link)

        TakipciCekTh = threading.Thread(target=TakipciCekThread)
        TakipciCekTh.start()

    def TakipEt(self):
        def TakipEtTh():
            
            browser = webdriver.Chrome("chromedriver.exe")
            browser.get("https://www.instagram.com")
            print("Çalıştım")
            user = self.ui.lineEdit.text()
            password = self.ui.lineEdit_2.text()
            time.sleep(2)
            browser.find_element_by_name("username").send_keys(user)
            browser.find_element_by_name("password").send_keys(password)
            browser.find_element_by_xpath(
                "//*[@id='loginForm']/div/div[3]/button/div").click()
            time.sleep(15)
            followLink = open("FollowersList.txt", "r")
            for userlink in followLink:
                browser.get(userlink)
                time.sleep(3)
                Follow_Button = browser.find_element_by_xpath("//*[text()='Follow']")
                print(Follow_Button.text)
                Follow_Button.click()
                time.sleep(3)
                
        TakipEtThread = threading.Thread(target=TakipEtTh)
        TakipEtThread.start()

    def HintButton(self):
        msg = QMessageBox()
        msg.setWindowTitle("Bilgilendirme")
        msg.setText("""
            *Şifre ve Kullanıcı Adı Girdikten Sonra İşlemleri Başlatabilirsiniz  
            *Kullanıcı Adı ve Şifre Kesinlikle Kaydedilmez ve Paylaşılmaz
            *Takipçilerini Çekmek İstediğiniz Kullanıcıları Aralarında Virgül Olacak Şekilde Yazın
            *Kullanıcı Çekimleri Bittikten Sonra Takip Et Butonuna Basarak Hepsini Takip Edebilirsiniz
            """)
        x = msg.exec_()


def app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MyApp()
    win.show()
    sys.exit(app.exec_())


app()
