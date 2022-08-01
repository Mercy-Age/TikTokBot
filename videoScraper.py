from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import subprocess
import youtube_dl
import time
import os

MAX_VIDEO_LENGTH = 60
URL = 'https://www.reddit.com/top/?t=day'

class ReditScraper():
    def __init__(self, video_folder):
        self.video_folder = video_folder
        self.videos = []

        # options is our setting for the webdriver
        # we work on Chrome
        options = webdriver.ChromeOptions()
        # its solve an error that can happend sometimes
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # to use Chrome driver with selenium we need to download chromedriver.exe from the internet
        self.driver = webdriver.Chrome(options=options, executable_path=r"C:\\chromedriver_win32\\chromedriver.exe")


    def open_web(self):
        try:
            self.driver.get(URL)
        except TimeoutException:
            self.driver.close()
            time.sleep(1)
            self.driver = webdriver.Chrome(options=options, executable_path=r"C:\\chromedriver_win32\\chromedriver.exe")
            self.driver.get(URL)
    
    def scroll_down(self, scrolls=2, scroll_pause_time=2):
        time.sleep(scroll_pause_time)
        
        screen_height = self.driver.execute_script("return window.screen.height;")
        for i in range(scrolls):
            self.driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")  
            time.sleep(scroll_pause_time)

    
    def get_videos_m3u8_link(self):
        # we will are using BeautifulSoup to find and filter the video's links 
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        body = soup.find("body")
        div = body.find("div")
        video_amount = len(div.find_all("video")) # how many videos tag there are in the page

        # what we are doing in this while is going down div tag by div tag to look for the
        # div tag that hold all of the posts
        # we know that if the div tag have less video tags then [video_amount] its mean that is the worng tag
        # so we will look for the div tag with video tags equal to [video_amount] and least div tags
        # this is the tag that will hold all of the posts 
        while True:
            divs = div.find_all("div")
            for i in range(len(divs)):
                if 'm3u8' in str(divs[i]):
                    new_div = divs[i]
                    break

            if not len(new_div.find_all("video")) == video_amount:
                break
            else:
                div = new_div


        # from here on we will start to filter individual posts
        divs = div.find_all("div")   
        posts = []
        skip = 0
        for i in range(len(divs)):
            # we check if there is a video file in this post (reddit use m3u8 type file)
            if 'm3u8' in str(divs[i]):
                if skip == 0:
                    skip = 7

                    # we remove promoted post
                    if not 'promoted' in str(divs[i]):
                        posts.append(divs[i])
                else:
                    skip -= 1

        # here we extract the videos from each post 
        if posts:
            for post in posts:
                title = post.find('div', style=lambda value: value and 'posttitletextcolor' in value)
                title_str = title.find('h3').text
                title_str = title_str.split('.')[0]
                video = post.find('video')
                link = video.find('source')['src']
                self.videos.append({'link':link, 'title':title_str})



    def load_videos(self):
        for video in self.videos:
            ydl_opts ={
                'outtmpl': self.video_folder+'\\'+ video['title'] +'.mp4',
                'format': ' bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video['link']])

            self.check_video_length()

    def get_length(self, path):
        # we check the length of the video if the video is 3 min long we will delete it
        # tiktok dose not accept videos that are 3 min or longer
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        if float(result.stdout) > MAX_VIDEO_LENGTH:
            os.remove(path)

    def check_video_length(self):
        video_names = os.listdir(self.video_folder)
        for name in video_names:
            self.get_length(self.video_folder+'\\'+name)

def main():
    RS = ReditScraper(video_folder='complete')
    RS.open_web()
    RS.scroll_down(scrolls=10)
    RS.get_videos_m3u8_link()
    #print(RS.videos)
    """
        'https://v.redd.it/ne1htrniun191/HLSPlaylist.m3u8?f=sd&v=1&a=1656147409%2CYzIxOGM1MzQyOTVhNWMwNjkyNDRmMGNiNTlmNzI0YTM3NDg3ZjBlNTU5M2U5NzQ0OGYyMmVhNjJmNzgzZTU2Nw%3D%3D'
        'https://v.redd.it/24m01hw6im191/HLSPlaylist.m3u8?f=hd&v=1&a=1656147409%2CYzZiZjIzOWE1MzgyYmQzM2NjMTk3YmJjZWEzZTU2ZTJmZGFkMzAzNTYwN2IzY2ExMzRmYTcxYjJjYmFiNjY5ZA%3D%3D'
        'https://v.redd.it/gefqtp33po191/HLSPlaylist.m3u8?f=sd&v=1&a=1656147409%2CMWRiMDIwMDVkMzA0OTUwYzM0NmVlZDhiZTMyZmQyYzEwNmNmMjI4YjUyMzJhYmFmN2U3MWM0MGFlMWM1MzJhOQ%3D%3D'
        'https://v.redd.it/au85wyk7io191/HLSPlaylist.m3u8?f=sd&v=1&a=1656147409%2CNTE0Y2YxNjk0ZGVjOTRlNDcxNjdkMGQ4NjAzM2I4MmQyM2IxNjMyZmE1ZWZlNzg3NWYwMmU3M2NkMWJlNTEyOQ%3D%3D'
    """
    RS.load_videos()



if __name__ == '__main__':
    main()