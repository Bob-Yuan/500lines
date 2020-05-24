import time

import requests

def google_captcha_local(page_url):
    server_url = "http://127.0.0.1:8080/get_captcha"
    data = {
        'page_url': page_url,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    while True:
        res = requests.post(server_url, data=data, headers=headers, timeout=20)
        if res.text == "CAPCHA_NOT_READY":
            print("谷歌人机验证，等待15s" + res.text)
            time.sleep(15)
        else:
            return res.text

page_url = "https://www.baidu.com"
#page_url = "https://www.google.com"
text = google_captcha_local(page_url)
print(text)
