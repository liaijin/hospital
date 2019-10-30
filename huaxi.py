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
    cookies = 'JSESSIONID=A30335F55487BF148F87AF6C065B8CB8'
    jar = dict()
    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        jar[key] = value

    requests.utils.add_dict_to_cookiejar(session.cookies, jar)
    print('获取cookie登录成功')


# 华西科室
def departmentList():
    # GET https://hytwechat.cd120.com/hyt/wechat/departmentList?area=F0005&today=0&hisCode=HID0101 HTTP/1.1
    # area=HID0101(华西院区) area=HID0103(温江院区) area=HIDW25(省五院区) area=F0005(芳草院区)
    print("请选择院区")
    print("1.华西院区")
    print("2.温江院区")
    print("3.省五院区")
    print("4.芳草院区")
    print("请选择需要预约的就诊卡(默认1)：", end='')
    k = int(input())
    global hisCode
    if k == 1:
        hisCode = 'HID0101'
    elif k == 2:
        hisCode = 'HID0103'
    elif k == 3:
        hisCode = 'HIDW25'
    elif k == 4:
        hisCode = 'F0005'
    else :
        hisCode = 'HID0101'
    departmentListUrl = 'https://hytwechat.cd120.com/hyt/wechat/departmentList?area=' + hisCode + '&today=1&hisCode=HID0101'
    r = session.get(departmentListUrl)
    soup = BeautifulSoup(r.text, "html.parser")
    # <div area="HID0101" class="deptList" hiscode="HID0101" resid="9300-MZMZ" today="1">麻醉专科门诊</div>
    deptList = soup.find_all("div", class_="deptList")
    for i in deptList:
        print('科室名称：' + i.text + ' resid：' + i['resid'])


# 华西就诊卡列表
def huaxiCardList(token, urUserId):
    print("开始获取就诊卡列表中......")
    '3410196_token_xxx_token_17898151636', '3410196'
    headers = {
        'Content-Type': 'application/json',
        'token': token
    }
    huaxiCardListUrl = 'https://hytapi.cd120.com/huayitong/card/query/cardList'
    data = {
        "organCode": "HID0101",
        "urUserId": "3410196",
        "channel": "WECHAT",
        "loading": 'false'
    }
    r = session.post(huaxiCardListUrl, headers=headers, data=json.dumps(data))
    if r.json()['success'] == True:
        print("就诊卡列表获取成功")
        cards = r.json()['data'][0]['cards']
        n = 1
        for i in cards:
            print("%d. 姓名：%s  医院：%s  卡号：%s" % (n, i['personName'], i['organName'], i['cardNo']))
        print("请选择需要预约的就诊卡(默认1)：", end='')
        k = input()
        global cardNo, cardName
        cardNo = cards[int(k) - 1]['cardNo']
        cardName = cards[int(k) - 1]['personName']
    else:
        print("就诊卡列表获取失败，失败原因%s", r.json()['message'])


# 科室医生列表
def doctorList(resid):
    # https://hytwechat.cd120.com/hyt/wechat/doctorlist/4300-XEWK?today=0&area=HID0101&hisCode=HID0101
    doctorListUrl = 'https://hytwechat.cd120.com/hyt/wechat/doctorlist/' + resid + '?today=0&area=HID0101&hisCode=HID0101'
    r = session.get(doctorListUrl)
    soup = BeautifulSoup(r.text, "html.parser")
    doctorList = soup.find_all("div", class_="doctorList")
    for i in doctorList:
        doctorCode = i['doctorcode']  # 医生代码
        clinic = i['clinic']
        doctorName = i.find('div', class_="doctorList_name")
        doctorLevel = i.find('div', class_="doctorList_title")
        isAvailable = '无号' if (i.find('div', class_="isAvailable").find('img')['src'].find('yh')) == -1 else '有号'
        print('医生名称：' + doctorName.text[0:len(doctorName.text) - len(
            doctorLevel.text)] + ' 级别：' + doctorLevel.text + ' 号源：' + isAvailable, doctorCode, clinic)


def doctorsDetail(a, b):
    doctorsDetailUrl = 'https://hytwechat.cd120.com/hyt/wechat/deptDoctorsDetail/4000-GK/' + a + '/' + b + '?today=0&area=HID0101&hisCode=HID0101'
    r = session.get(doctorsDetailUrl)
    soup = BeautifulSoup(r.text, "html.parser")
    docinfo = soup.find('div', class_="docdetail_docinfo")
    print('医生名称：', docinfo.div.string)
    scheduleList = soup.find_all('div', class_="scheduleList")
    for i in scheduleList:
        detailJson = json.loads(i['data-meta'])
        detailUser = i['data-user']
        print(detailUser, detailJson['resourceId'], detailJson['serviceDate'], detailJson['timeRang'],
              detailJson['regAvailable'])


def appointment():
    appointmentUrl = 'https://hytwechat.cd120.com/hyt/wechat/requestAppointment'
    data = {
        "hisCode": "HID0101",
        "resourceId": "1182||1252",
        "patientId": "20660942",
        "cardNo": "030000000604956",
        "captcha": "3629",
        "captchaId": "1567760350434638648"
    }
    headers = {
        'Host': 'hytwechat.cd120.com',
        'Connection': 'keep-alive',
        'Content-Length': '148',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://hytwechat.cd120.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
        'Content-Type': 'application/json',
        'Referer': 'https://hytwechat.cd120.com/hyt/wechat/appointmentRequest/1182%7C%7C1255?today=0&checkType=1&hisCode=HID0101',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4'
    }
    r = session.post(appointmentUrl, headers=headers, data=json.dumps(data))
    # 预约成功json格式
    # code:0 为失败 code:1为成功
    # {"code":"1","msg":"请求预约挂号成功","confirmAppVo":{"patientName":"李艾劲","patientNo":"030000000604956","apptDate":"2019-09-19","hospitalName":"四川大学华西医院","hospitalCode":"HID0101","appointType":null,"apptAddress":"门诊大楼二楼E区11诊室-11诊室","departmentName":"骨科医疗单元","doctorName":"康鹏德","price":"92.0","fetchEndTime":null,"takeAddress":"门诊自助机或大门诊二、三楼F区挂号窗口取号","patientSex":null,"sequenceNo":"40","visitNo":null,"orderId":null,"timeRange":"10:30-11:00","timeout":null,"appointmentId":"1182||1255||47","hisAppId":null,"hospitalAddress":"成都市武侯区国学巷37号","passkey":null,"resourceId":"1182||1255","patientId":"20660942","status":"2","appointTime":"1567758756767","canPay":"true","canCancel":"true","canRefund":"false","channelCode":"微信","regionHospIDs":"1","autoCollect":"1","dealSeq":"010051067920190906043236740","merchantSeq":"HID0101","bizSysSeq":"hytYYGH01","oldOrderFlag":"0"}}
    print(r.text)


def captcha(hisCode):
    captchaUrl = 'https://hytwechat.cd120.com/hyt/wechat/captcha'
    data = {"hisCode": hisCode, "captchaType": "REQ_APPOINTMENT"}
    r = session.post(captchaUrl, data=json.dumps(data))
    print('开始获取验证码')
    print(r.json()['msg'], ' 验证码ID:', r.json()['data']['captchaId'])
    file_img = open(('captcha(' + r.json()['data']['captchaId'] + ').jpg'), 'wb')
    file_img.write(base64.b64decode(r.json()['data']['captchaImg']))
    file_img.close()


# def shibie():


getCookie()
#huaxiCardList('3410196_token_xxx_token_17898151636', '3410196')
print("")
#departmentList()
#doctorList('4201-XWK')
doctorsDetail('17442','294')
# appointment()
# captcha('HID0101')
exit()
