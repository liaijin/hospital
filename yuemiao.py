import requests
import json
import base64
from bs4 import BeautifulSoup

session = requests.Session()

# 就诊卡号
cardNo = ''
# 就诊卡姓名
cardName = ''
# 院区
hisCode = ''


# 获取cookie
def getCookie():
    cookies = 'UM_distinctid=16d7197d899868-0cfc101164db1a-4a145c7d-1fa400-16d7197d89a4f6; _xzkj_=966f4478ff6317ba86c6b8429b1aaa6c_e82c325032e9b2a0bc42eed27f66ab55; _xxhm_=%7B%22address%22%3A%22%22%2C%22awardPoints%22%3A0%2C%22birthday%22%3A795801600000%2C%22createTime%22%3A1561078399000%2C%22headerImg%22%3A%22http%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2FQ3auHgzwzM7rattnic0HnNxTibjuBJjcTOhgQwibzUwwMojf5YPKJNBiaianfZKLQG2rOuawicwJy4OKBhMOPBkI6zNsBZWP6RMdpvwsSNIERP2jk%2F132%22%2C%22id%22%3A3184054%2C%22idCardNo%22%3A%22%22%2C%22isRegisterHistory%22%3A0%2C%22latitude%22%3A0.0%2C%22longitude%22%3A0.0%2C%22mobile%22%3A%2215196656006%22%2C%22modifyTime%22%3A1569569579000%2C%22name%22%3A%22%E7%89%9F%E5%B0%8F%E7%BF%A0%22%2C%22nickName%22%3A%22%E5%A4%9C%E9%98%91%E5%B0%8F%E9%9B%A8%22%2C%22openId%22%3A%22og46NxPVBCSmJvEWx0MbAzbXIKRE%22%2C%22regionCode%22%3A%220%22%2C%22registerTime%22%3A1569568878000%2C%22sex%22%3A2%2C%22source%22%3A1%2C%22uFrom%22%3A%22depa_vacc_detail%22%2C%22unionid%22%3A%22o8NLkwf6Myblf34oE4pXy-pZVL9k%22%2C%22wxSubscribed%22%3A1%2C%22yn%22%3A1%7D; CNZZDATA1261985103=410261128-1569566986-https%253A%252F%252Fopen.weixin.qq.com%252F%7C1569566986'
    jar = dict()
    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        jar[key] = value

    requests.utils.add_dict_to_cookiejar(session.cookies, jar)
    print('获取cookie登录成功')


# 获取医院信息
def departmentList():
	departmentUrl = 'https://wx.healthych.com/base/department/pageList.do?vaccineCode=8803&cityName=&offset=0&limit=10&name=&regionCode=5101&isOpen=1&longitude=&latitude='
	headers = {
	'Host': 'wx.healthych.com',
	'Connection': 'keep-alive',
	'Accept': 'application/json, text/plain, */*',
	'tk': '966f4478ff6317ba86c6b8429b1aaa6c_e82c325032e9b2a0bc42eed27f66ab55',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
	'st': 'd762b8e16dcefe24d8ba14955483bd07',
	'Referer': 'https://wx.healthych.com/index.html',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
	}
	
	r = session.get(departmentUrl, headers=headers)
	if r.json()['code']=='3101':
		print('用户登录超时,请重新登入!')
		return 0
	for i in r.json()['data']['rows']:
		print('医院名称：%s  数量：%s' % (i['name'],i['total']))
	
# def shibie():


getCookie()
departmentList()

exit()
