import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains



URL = 'https://www.tiktok.com/'

class Subscribe():
    def __init__(self):
        # options is our setting for the webdriver
        # we work on Chrome
        options = webdriver.ChromeOptions()
        # its solve an error that can happend sometimes
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # this options use our Chrome user data when we open the driver 
        # we use this options so we would not need to log in everytime 
        # we only need to log in once me manually 
        options.add_argument('user-data-dir=C:\\Users\\AppTeam\\AppData\\Local\\Google\\Chrome\\User Data')

        # to use Chrome driver with selenium we need to download chromedriver.exe from the internet
        self.driver = webdriver.Chrome(options=options, executable_path=r"C:\\chromedriver_win32\\chromedriver.exe")

    def open_web(self):
        try:
            self.driver.get(URL)
        except TimeoutException:
            # if there is an error close and try again
            self.driver.close()
            time.sleep(1)
            self.driver = webdriver.Chrome(options=options, executable_path=r"C:\\chromedriver_win32\\chromedriver.exe")
            self.driver.get(URL)
        time.sleep(2)

    
    def scroll_down(self, scrolls=2, scroll_pause_time=2):
        time.sleep(scroll_pause_time)
        
        screen_height = self.driver.execute_script("return window.screen.height;")
        for i in range(scrolls):
            self.driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")  
            time.sleep(scroll_pause_time)


    def subscribe_and_like(self):
        follow_elements = self.driver.find_elements(By.XPATH, '//button[text()="Follow"]')
        #the header hidde the first element so we use a different code for it
        e = follow_elements.pop(0)
        actions = ActionChains(self.driver)
        actions.move_to_element(e)
        actions.click(on_element = e)
        actions.perform()
        time.sleep(1)

        for element in follow_elements:
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(element, 0,-600)
            actions.pause(1)
            actions.click(on_element = element)
            actions.perform()
            time.sleep(1)

        time.sleep(5)



