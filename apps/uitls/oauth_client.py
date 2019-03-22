# import json
# import urllib, urllib2, urlparse
#
# class OAuth_QQ():
#     def __init__(self, client_id, client_key, redirect_uri):
#         self.client_id = client_id
#         self.client_key = client_key
#         self.redirect_uri = redirect_uri
#
#     def get_auth_url(self):
#         """获取授权页面的网址"""
#         params = {'client_id': self.client_id,
#                   'response_type': 'code',
#                   'redirect_uri': self.redirect_uri,
#                   'scope': 'get_user_info',
#                   'state': 1}
#         url = 'https://graph.qq.com/oauth2.0/authorize?%s' % urllib.urlencode(params)
#         login_url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=%s&%s&state=%s' % (
#             client_id, callback, state)
#         return url