'''
Created by auto_sdk on 2019.10.15
'''
from top.api.base import RestApi
class TbkDgMaterialOptionalRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.adzone_id = None
		self.cat = None
		self.device_encrypt = None
		self.device_type = None
		self.device_value = None
		self.end_ka_tk_rate = None
		self.end_price = None
		self.end_tk_rate = None
		self.has_coupon = None
		self.include_good_rate = None
		self.include_pay_rate_30 = None
		self.include_rfd_rate = None
		self.ip = None
		self.is_overseas = None
		self.is_tmall = None
		self.itemloc = None
		self.lock_rate_end_time = None
		self.lock_rate_start_time = None
		self.material_id = None
		self.need_free_shipment = None
		self.need_prepay = None
		self.npx_level = None
		self.page_no = None
		self.page_size = None
		self.platform = None
		self.q = None
		self.sort = None
		self.start_dsr = None
		self.start_ka_tk_rate = None
		self.start_price = None
		self.start_tk_rate = None

	def getapiname(self):
		return 'taobao.tbk.dg.material.optional'
