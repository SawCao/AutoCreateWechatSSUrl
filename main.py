# -- coding: utf-8 --
import requests
import sys
import time
import logging
import pyperclip
from requests_toolbelt import MultipartEncoder
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
            if "微信截图" in event.src_path:
                headers = {"Connection": "keep-alive",
                           "Content-Length": "25713",
                           "Accept": "application/json, text/javascript, */*; q=0.01",
                           "Origin": "https://sm.ms",
                           "X-Requested-With": "XMLHttpRequest",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                           "Referer": "https://sm.ms/",
                           "Accept-Encoding": "gzip, deflate, br",
                           "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"}

                time.sleep(2)
                print(event.src_path)
                filePath = event.src_path
                print(filePath)
                file_payload = {'smfile':("xxx.png",open(event.src_path,'rb'),"image/png")}
                m = MultipartEncoder(file_payload)
                headers['Content-Type'] = m.content_type

                r = requests.post('https://sm.ms/api/upload?inajax=1&ssl=1', data=m,
                                  headers=headers, verify=False)
                print(r.json())
                pyperclip.copy(r.json()['data']['url'])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = 'D:\sub_photo'
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
