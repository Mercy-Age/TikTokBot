import time
import cv2 as cv
import numpy as np
from collections import Counter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class VideoDeleter():
    def __init__(self):
        self.videos_to_delete = []

        # options is our setting for the webdriver
        # we work on Chrome
        self.options = webdriver.ChromeOptions()
        # its solve an error that can happend sometimes
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # this options use our Chrome user data when we open the driver 
        # we use this options so we would not need to log in everytime 
        # we only need to log in once me manually 
        self.options.add_argument('user-data-dir=C:\\Users\\AppTeam\\AppData\\Local\\Google\\Chrome\\User Data')

        # to use Chrome driver with selenium we need to download chromedriver.exe from the internet
        # self.driver = webdriver.Chrome(options=options, executable_path=r'C:\\chromedriver_win32\\chromedriver.exe')

    def open_web(self, url):
        try:
            self.driver = webdriver.Chrome(options=self.options, executable_path=r'C:\\chromedriver_win32\\chromedriver.exe')
            self.driver.get(url)
        except TimeoutException:
            self.driver.close()
            time.sleep(1)
            self.driver = webdriver.Chrome(options=options, executable_path=r'C:\\chromedriver_win32\\chromedriver.exe')
            self.driver.get(url)
        time.sleep(2)

    def close_web(self):
        self.driver.close()
        time.sleep(2)

    def scroll_down(self, scrolls=2, scroll_pause_time=2):
        time.sleep(scroll_pause_time)
        
        screen_height = self.driver.execute_script("return window.screen.height;")
        for i in range(scrolls+1):
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            time.sleep(scroll_pause_time)

    def find_videos_to_delete(self, min_views=0):
        self.scroll_down()

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        body = soup.find('body')
        #data-e2e="user-post-item-list"
        div = body.find('div', {'data-e2e':'user-post-item-list'})
        # becouse tiktok change change their classes we will use the first post to find the others
        first_post = div.find('div')
        posts_class = " ".join(first_post['class'])
        posts = div.find_all('div', {'class': posts_class}) # a list of all of our posts

        # now that we have our posts we can filter which one we want to delete and get its link
        for post in posts:
            views = post.find('strong', {'data-e2e':'video-views'})
            views = int(views.text)
            if views <= min_views:
                link = post.find('a')['href']
                self.videos_to_delete.append(link)

    def delete_videos(self):
        for link in self.videos_to_delete:
            self.open_web(link)
            time.sleep(2)

            # we click on the video to get to the video setting
            video = self.driver.find_element(By.XPATH, '//video')
            video.click()
            
            self.solve_captcha()
            
            # we need to over on the setting sign (the "..." icon) if we when the delete button to appear
            element_to_hover_over = self.driver.find_element(By.XPATH, '//div[@data-e2e="video-setting"]')
            hover = ActionChains(self.driver).move_to_element(element_to_hover_over)
            hover.perform()
            time.sleep(1)

            # we click the delete button
            self.click_delete()

            # after we click delete its will ask "are you sure you want delete"
            # which is why we need to click delete twice
            self.click_delete()

            self.close_web()
    

    def click_delete(self):
        delete_button = self.driver.find_element(By.XPATH, '//button[text()="Delete"]')
        delete_button.click()
        time.sleep(1)

    def solve_captcha(self):
        print('solving captcha')
        # wait for the captcha to load
        for i in range(11):
            try:
                # if find_element cant find the element its will raise an error
                img = self.driver.find_element(By.ID,"captcha-verify-image")
                if img.get_attribute('src'):
                    time.sleep(1)
                    # take a screen shot of the captcha
                    img.screenshot('temp.png')
                    break
            except:
                if i == 10:
                    
                    print("==========================================")
                    print("took too long to load")
                    print("==========================================")
                    return "captcha did not load"
                time.sleep(1) 

        time.sleep(1)
        img = cv.imread('temp.png')
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        corners = cv.goodFeaturesToTrack(gray,15,0.05,1)
        corners = np.int0(corners)
        
        x_Array = []
        for i in corners:
            x,y = i.ravel()
            if x > 70:
                x_Array.append(x)

        x_Array.sort()

        source = self.driver.find_element(By.CLASS_NAME,"secsdk-captcha-drag-icon")

        unic = Counter(x_Array)
        for x in x_Array:
            if unic[x] > 1:
                x_offset = x-8
                break

        action = ActionChains(self.driver)
        try:
            steps_count = 5
            step = (x_offset)/steps_count
            act_1 = action.click_and_hold(source)
            for _ in range(0,steps_count):
                act_1.move_by_offset(step, 0)
            act_1.release().perform()

            msg = self.driver.find_element(By.CLASS_NAME,'msg').find_element(By.TAG_NAME,'div').text
            while msg == '':
                msg = self.driver.find_element(By.CLASS_NAME,'msg').find_element(By.TAG_NAME,'div').text
            if msg == "Unable to verify. Please try again.":
                print("failed to verify. will try again in 2 sec")
                time.sleep(2)
                self.solve_captcha()

            print('finish captcha')

        except Exception as e:
            print('================================')
            print(e)
            print('================================')


if __name__ == '__main__':
    VD = VideoDeleter()
    VD.open_web("https://www.tiktok.com/@cupjuice27?lang=en")
    VD.find_videos_to_delete()
    VD.close_web()
    VD.delete_videos()