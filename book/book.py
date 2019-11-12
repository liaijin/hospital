import requests
import os
import json
import base64
from bs4 import BeautifulSoup

session = requests.Session()


def get_img(book_id, number):
    r = session.get('http://www.bm819k.cn/index/book/read.html?book_id=' + book_id + '&number=' + number)
    soup = BeautifulSoup(r.text, "html.parser")
    img_class = soup.find("div", class_="imgCount")
    img_list = img_class.find_all("img")
    n = 1
    for i in img_list:
        img_down(i['src'], (book_id + "/" + number), str(n) + ".jpg")
        n = n + 1


def img_down(url, path, fina_name):
    if not os.path.exists(path):
        os.makedirs(path)
        print("目录创建成功 " + path)
    r = session.get(url)
    print(fina_name)
    # 验证码保存本地
    file_img = open((path + "/" + fina_name), 'wb')
    file_img.write(r.content)
    file_img.close()

for i in range(1, 11):
    print(i)
    #get_img("88", str(i))

# doctorsDetail('15372','220')
# appointment()
# captcha('HID0101')
exit()
