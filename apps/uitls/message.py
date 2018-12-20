#!/usr/bin/python  
# -*- coding:utf-8 -*-  
# 短信应用SDK AppID
appid = 1400170764  # SDK AppID是1400开头

# 短信应用SDK AppKey
appkey = "3c9dcc0da5aa6bb4d24eb09197db21ee"

# 需要发送短信的手机号码
phone_numbers = ["18381753236", "12345678902", "12345678903"]

# 短信模板ID，需要在短信应用中申请
template_id = 7839  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
# templateId 7839 对应的内容是"您的验证码是: {1}"
# 签名
sms_sign = "腾讯云"  # NOTE: 这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`


from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

ssender = SmsSingleSender(appid, appkey)
params = ["5678"]  # 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
try:
    result = ssender.send_with_param(86, phone_numbers[0],
        template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)

print(result)