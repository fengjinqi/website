'''
Created by auto_sdk on 2018.07.25
'''
from top.api.base import RestApi
class TmcMsgSendrecordRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.data_id = None
		self.group_name = None
		self.topic_name = None

	def getapiname(self):
		return 'taobao.tmc.msg.sendrecord'
