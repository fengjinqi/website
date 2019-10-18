'''
Created by auto_sdk on 2018.07.25
'''
from top.api.base import RestApi
class AlipayXiaodaiUserPermitRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.user_id = None

	def getapiname(self):
		return 'alipay.xiaodai.user.permit'
