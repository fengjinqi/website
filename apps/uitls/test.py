import requests
#res = requests.get('https://www.biqiuge.com/book/4772/')
#print(res.content.decode("gbk"))
"""

ser = '剑起风云'

header = {
    'ie':'gbk',
    'siteid':'biqiuge.com',
    's':'2758772450457967865',
    'q':ser.encode('gbk')
}
res = requests.get('https://so.biqusoso.com/s.php',header)
print(res.content.decode('utf8'))
"""


res = requests.get('https://www.biqushu.com/book_107713/44411383.html')
print(res.content.decode('gbk'))