import requests


# 登录接口
def login():
    # phoneNumber=13312345678&password=cF3myMHlGxMQ9pvXsWPBGw%3D%3D&memberid=&memberId=&mobile=&token=&language=zh&store=003
    print("请输入登录的手机号码(密码默认为123123)：", end='')
    phone_number = input()
    data = {
        "phoneNumber": phone_number,
        "password": "cnssWAVm2vAIoeXDiVDHjw=="
    }
    print("请稍等，正在登录中.....")
    r = requests.post("https://crm.iy-cd.com/wns-ciycrmapp/appLoginController/passwordLogin", data=data)
    result = r.json()
    # print(r.json())
    if result['flag']:
        if len(result['result']) == 3:
            print("恭喜你，账号" + result['result']['phoneNumber'] + "登录成功")
            return phone_number, result['result']['memberid'], result['result']['token']
    else:
        print('账号登录失败,', result['message'])
        print("按任意键退出!!!", end='')
        input()
        exit()


def getStore():
    # 请求值 memberid=9520038000335&memberId=9520038000335&mobile=13408081070&token=0445CAF7C70D7875ACBD769731CF2DC5&language=zh&store=003
    r = requests.post("https://crm.iy-cd.com/wns-ciycrmapp/appLoginController/getStorem")
    # 返回值 {"flag":true,"message":"操作成功!","result":{"storem":[{"text":"春熙店","value":"001"},{"text":"双楠店","value":"002"},{"text":"锦华店","value":"003"},{"text":"建设路店","value":"004"},{"text":"高新店","value":"005"},{"text":"温江店","value":"006"},{"text":"眉山店","value":"007"},{"text":"绿地店","value":"008"},{"text":"华府大道店","value":"101"}]},"count":0}
    if r.json()['flag']:
        n = 1
        rr = r.json()['result']['storem']
        print("请选择店铺")
        for i in rr:
            print(str(n) + '. ' + i['text'])
            n = n + 1
        print("请选择领取的店铺：", end='')
        k = int(input())
    return rr[k - 1]['text'], rr[k - 1]['value']


def goodsList():
    r = requests.get(
        "https://crm.iy-cd.com/wns-ciycrmapp/appHomeController/getPointsChangeList?giftKbn=-1&orderBy=3&storeCode=003&token=0445CAF7C70D7875ACBD769731CF2DC5")

    if r.json()['flag']:
        n = 1
        rr = r.json()['result']
        print("请选择商品")
        for i in rr:
            print(str(n) + '. ' + i['goodsName'] + '(' + str(i['goodsCount']) + ')')
            n = n + 1
        print("请选择兑换的商品：", end='')
        k = int(input())
    return rr[k - 1]['recordid'], rr[k - 1]['goodsId'], rr[k - 1]['eid']


# 下单
def ocrCaptcha(recordid, goodsId, eid, storeId, memberid1, token1):
    # recordid=244&goodsId=493&eid=574&pikeId=&memberid=9520038000335&memberId=9520038000335&mobile=13408081070&token=0445CAF7C70D7875ACBD769731CF2DC5&language=zh&store=003&changeCount=1&storeId=003
    data = {
        "recordid": recordid,
        "goodsId": goodsId,
        "eid": eid,
        "changeCount": "1",
        "storeId": storeId,
        "memberid": memberid1,
        "token": token1
    }
    r = requests.post("https://crm.iy-cd.com/wns-ciycrmapp/appHomeController/doPointsChange", data=data)
    # print(r.json())
    return r.json()


# 登录
phone_number, memberid, token = login()

# 获取店铺
store_name, store_id = getStore()
print("获取店铺成功：", store_name)
user_info = [
    {
        "name": phone_number,
        "memberid": memberid,
        "token": token
    }
]

# 获取选择商品信息
recordid, goodsId, eid = goodsList()
num = 1
# 默认从第一个用户开始
user_num = 0
for i in range(1, 10000):

    result = ocrCaptcha(recordid, goodsId, eid, store_id, user_info[user_num]['memberid'], user_info[user_num]['token'])
    if result['flag']:
        if not result['result']:
            print('第' + str(num) + '次抢购失败，', result['message'])
            num = num + 1
        else:
            print(user_info[user_num]['name'] + '用户抢购成功，请前往兑换中心查看!!!')
            if user_num + 1 == len(user_info):
                print('所有用户抢购完成，请前往兑换中心查看!!!')
                break
            else:
                user_num = user_num + 1
    else:
        print('抢购失败,', result['message'])
        break

print("按任意键退出!!!", end='')
input()
