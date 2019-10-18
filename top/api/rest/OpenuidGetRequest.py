'''
Created by auto_sdk on 2018.10.17
'''
from top.api.base import RestApi
class OpenuidGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.openuid.get'
