import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


URL = 'https://www.tiktok.com/upload?lang=en'

class VideoUploader():
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

    def upload(self, path: str, file_name: str):
        self.open_web()
        self.upload_video(path=path, file_name=file_name)
        self.post(file_name=file_name)
        self.driver.close()

    def open_web(self):
        try:
            self.driver.get(URL)
        except TimeoutException:
            self.driver.close()
            time.sleep(1)
            self.driver = webdriver.Chrome(options=options, executable_path=r"C:\\chromedriver_win32\\chromedriver.exe")
            self.driver.get(URL)
        time.sleep(2)

    def upload_video(self, path: str, file_name: str):
        """
            path is the path to the video file from the place the script in (not includes the file name)
            for example: if "C:\\Users\\AppTeam\\Desktop\\New folder\\video\\complete\\Mike is a good guy.mp4"
            is our full path and the script is in "New folder" then:
            path = "\\video\\complete\\"
            file_name = "Mike is a good guy.mp4"
        """

        # Button is nested in iframe document. Select iframe first then select upload button
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        self.driver.switch_to.frame(0)
        self.driver.implicitly_wait(1)

        # we serch for input with a type file in, it there should only be one and we upload to it  
        file_input_element = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input_element.send_keys(os.getcwd()+path+file_name)


    def post(self, file_name: str):
        # wait for Post button to be clickable
        while True:
            page = self.driver.page_source
            if file_name in page and not "Uploading " + file_name in page:
                break
            time.sleep(1)

        # add hastagh
        inputElement = self.driver.find_element(By.XPATH, '//span[@data-text="true"]')
        inputElement.send_keys(' #fyp #foryoupage')

        # click the button with text = "Post" in it 
        # file_post_element = self.driver.find_element(By.XPATH, '//button[text()="Post"]')
        # file_post_element.click()
        # time.sleep(2)

if __name__ == '__main__':
    VU = VideoUploader()
    VU.upload(path="\\complete\\", file_name="Making A Brass Extension For Severed Thumb.mp4")