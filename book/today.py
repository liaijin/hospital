# 今日头条字符串加密
def encrypt(e):
    s = ""
    for i in e:
            s = s + hex(5 ^ ord(i))[2:]
    return s


print(encrypt("Li135246"))
