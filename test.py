import json
data = [
    {"com": "恒瑞医药", "pro": "多西他赛"},
    {"com": "恒瑞医药", "pro": "奥沙利铂"},
    {"com": "恒瑞医药", "pro": "伊立替康"},
    {"com": "恒瑞医药", "pro": "来曲唑"},
    {"com": "恒瑞医药", "pro": "亚叶酸钙"},
    {"com": "恒瑞医药", "pro": "七氟烷"},
    {"com": "恒瑞医药", "pro": "碘佛醇"},
    {"com": "恒瑞医药", "pro": "厄贝沙坦"},
    {"com": "恒瑞医药", "pro": "右美托咪定"},
    {"com": "恒瑞医药", "pro": "苯磺顺阿曲库铵"},
    {"com": "华东医药", "pro": "阿卡波糖"},
    {"com": "华东医药", "pro": "泮托拉唑"},
    {"com": "华东医药", "pro": "环孢素A"},
    {"com": "华东医药", "pro": "吗替麦考酚酯"},
    {"com": "华东医药", "pro": "吡格列酮/二甲双胍"},
    {"com": "华东医药", "pro": "吡格列酮"},
    {"com": "华东医药", "pro": "他克莫司"},
    {"com": "华东医药", "pro": "百令胶囊"},

]
import re
# example = json.load(data)
# for d in data:
#     print(d['com'], d['pro'])
# total = '5'
# page = int(int(total) / 20) + 1
# print(page)
url = 'https://db.yaozh.com/yaopinzhongbiao?name={0}&zb_shengchanqiye={1}&first={2}&pageSize=20&p=20'
url = re.subn('p=\d+', 'p=5', url)
print(url)