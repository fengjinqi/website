import os
from configparser import ConfigParser
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'config.ini')
import top.api
conf = ConfigParser()
conf.read(BASE_DIR)



# req=top.api.JuItemsSearchRequest('http://127.0.0.1','8000')
# req.set_app_info(top.appinfo(conf.get('taobao','appkey'),conf.get('taobao','secret')))
# header = {
# 	"current_page":1,
# 	"page_size":20,
# 	"pid":'',
# 	"postage":True,
# 	"status":2,
# 	"taobao_category_id":'973700308',
# 	"word":''
# }
# req.param_top_item_query=header
# try:
# 	resp= req.getResponse()
# 	print('',resp)
# except Exception as e:
# 	print('error',e)


req=top.api.TbkUatmFavoritesGetRequest()
req.set_app_info(top.appinfo(conf.get('taobao','appkey'),conf.get('taobao','secret')))

req.page_no=1
req.page_size=20
req.fields="favorites_title,favorites_id,type"
req.type=-1
resp= req.getResponse()
print(resp)

# try:
# 	resp= req.getResponse()
# 	print(resp)
# except Exception as e:
# 	print(e)