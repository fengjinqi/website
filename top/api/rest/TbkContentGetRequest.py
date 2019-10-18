'''
Created by auto_sdk on 2019.07.04
'''
from top.api.base import RestApi
class TbkContentGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.adzone_id = None
		self.before_timestamp = None
		self.cid = None
		self.content_set = None
		self.count = None
		self.image_height = None
		self.image_width = None
		self.type = None

	def getapiname(self):
		return 'taobao.tbk.content.get'
