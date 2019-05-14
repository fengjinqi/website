from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


# class ZxMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         if 'HTTP_X_FORWARDED_FOR' in request.META:
#             ip = request.META['HTTP_X_FORWARDED_FOR']
#         else:
#             ip = request.META['REMOTE_ADDR']
#         online_ips = cache.get("online_ips", [])
#         if online_ips:
#             online_ips = cache.get_many(online_ips).keys()
#
#         cache.set(ip, 0, 5 * 60)
#
#         if ip not in online_ips:
#             online_ips.append(ip)
#         print(online_ips)
#         cache.set("online_ips", online_ips)