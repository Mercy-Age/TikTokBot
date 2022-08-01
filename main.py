from uploadTiktok import VideoUploader
from videoScraper import ReditScraper
from subTiktok import Subscribe
import argparse
import os

# if you want to use this app you will need chrome and chromedriver
# the chromedriver need to at "C:\\chromedriver_win32\\chromedriver.exe"
# you will need chromedriver that fit your chrome version

parser = argparse.ArgumentParser()
parser.add_argument('-d','--download', action='store_true', help="download videos from reddit")
parser.add_argument('-u','--upload', action='store_true', help="upload videos from the complete fodler to tiktok")
parser.add_argument('-s', action='store_true', help="like random post on tiktok and subscribe to random channels")
args = vars(parser.parse_args())


VIDEOFOLDER = "complete"

# downloads videos from reddit most popular videos of today
def download():
    RS = ReditScraper(video_folder=VIDEOFOLDER)
    RS.open_web()
    RS.scroll_down(scrolls=10)
    RS.get_videos_m3u8_link()
    RS.load_videos()

# upload videos to tiktok
def upload():
    video_names = os.listdir(VIDEOFOLDER)
    for name in video_names:
        VU = VideoUploader()
        VU.upload(path=f"/{VIDEOFOLDER}/", file_name=name)
        os.remove(f"{VIDEOFOLDER}\\{name}")

# like random post on tiktok and subscribe to random channels
def subscribe():
    sub = Subscribe()
    sub.open_web()
    # the more you scroll down the more post you will like and sub to
    sub.scroll_down(scrolls=10)
    sub.subscribe_and_like()


def main():
    if args['download']:
        download()

    if args['upload']:
        upload()
    if args['s']:
        subscribe()

if __name__ == '__main__':
    main()