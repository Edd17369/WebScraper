# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 19:13:08 2020

@author: faust
"""

# C:\Users\faust\AppData\Roaming\Python\Python37\site-packages\instapy

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time

# Abre Instagram en firefox e inicia sesión
browser = webdriver.Firefox(executable_path = r'C:/geckodriver/geckodriver.exe')
browser.get('https://www.instagram.com/')

time.sleep(5)

# Login
try:
    loginUser = browser.find_element_by_name('username')
    loginPass = browser.find_element_by_name('password')
    loginSubmit= browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
    try:
        loginUser.send_keys('falsodonfalso@gmail.com')
        loginPass.send_keys('waffles1783')
        loginSubmit.send_keys(Keys.ENTER)
    except:
        print('Check your login information!')
except:
    print('Cannot find login elements!')


time.sleep(5)

# Elige no gurdar la información de sesión !!!!!!


# Notificaciones  
try:
    notif = browser.find_elements_by_tag_name('button')
    #notifON = notif[-2]
    notifOFF = notif[-1]
    # y_n = input()
    # if y_n == y:
    # notifON.send_keys(Keys.ENTER)
    # print('Notifications activated')
    # else:
    notifOff.send_keys(Keys.ENTER)
    print('Notifications deactivated')
except:
    print('Ya elegiste tu configuracion sobre notificaciones')

time.sleep(5)

# Busca publicaciones con mas de 100,000 'Me gusta'

number_of_likes = 0
while number_of_likes < 100: # cuantos likes das por sesion
    ilike = browser.find_elements_by_partial_link_text('Me gusta')
    meGusta = browser.find_elements_by_css_selector('button > div > span > svg')

    for item in numMegusta:
        if len(item.text) > 15 and 'Me gusta' in item.text:
            # click 'Me Gusta'
            for i in range(0, len(meGusta)):
                aria_label = meGusta[i].get_attribute('aria-label')
                height =  meGusta[i].get_attribute('height')
                if aria_label == 'Me gusta' and height == '24':
                    meGusta[i].click()
                    number_of_likes += 1              
    html.send_keys(Keys.PAGE_DOWN)



    
