import execjs
import requests
import os
import json
import base64
from bs4 import BeautifulSoup

session = requests.Session()


def login(username, password):
    headers={
        "Content-Type": "application/json"
    }
    user_data = {
            "userName": "17898151636",
            "password": "00737b8ed1587ba353d545464f55129e0eb3fb26",
            "remember": "1",
            "behavior": "%5B%7B%22page.login%22%3A%220.063%22%7D%2C%7B%22input.l.account%22%3A%221.349%22%7D%2C%7B%22input.l.passwd%22%3A%225.371%22%7D%2C%7B%22input.l.passwd%22%3A%228.563%22%7D%2C%7B%22button.UDBSdkLogin%22%3A%228.69%2C277%2C211%22%7D%2C%7B%22button.UDBSdkLogin%22%3A%2214.293%2C202%2C210%22%7D%2C%7B%22input.l.passwd%22%3A%2278.719%22%7D%2C%7B%22input.l.passwd%22%3A%2281.761%22%7D%2C%7B%22button.UDBSdkLogin%22%3A%2281.861%2C152%2C225%22%7D%2C%7B%22button.UDBSdkLogin%22%3A%22144.541%2C144%2C220%22%7D%2C%7B%22input.l.passwd%22%3A%221173.691%22%7D%2C%7B%22button.UDBSdkLogin%22%3A%221179.049%2C211%2C229%22%7D%2C%7B%22input.l.passwd%22%3A%222826.343%22%7D%2C%7B%22button.UDBSdkLogin%22%3A%222834.897%2C241%2C213%22%7D%5D",
            "page": "https://www.huya.com/"
        }
    data = {
        "uri": "30001",
        "version": "2.4",
        "appId": "5002",
        "byPass": "3",
        "data": user_data
    }
    r = session.post('https://udblgn.huya.com/web/v2/passwordLogin',headers=headers, data=json.dumps(data))
    for c in r.cookies:
        print(c)
    print(r.json())
    rr=session.get("https://i.huya.com/")
    print(rr.text)


def get_js():
    f = open("js/huya.js", 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr


def get_des_psswd():
    jsstr = get_js()
    ctx = execjs.compile(jsstr)  # 加载JS文件
    return (ctx.call('encode', 'li13524'))

login(1,2)

#print(get_des_psswd())
