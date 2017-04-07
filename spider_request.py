# coding:utf-8
import requests
from lxml import html
import re
import pymysql
import os
import time


urls = 'https://db.yaozh.com/yaopinzhongbiao?name={0}&zb_shengchanqiye={1}&first={2}&pageSize=20&p={3}'
first = '全部'
p = '1'

cookies = {'PHPSESSID=169t3qjps2uadhdlu7q6nrl020; MEIQIA_EXTRA_TRACK_ID=0070956c107b11e7a7c00246fd076266; WAF_SESSION_ID=f2e50c98c8ba11854406efcb42a09786; mylogin=1; UtzD_f52b_saltkey=oWr2AyrG; UtzD_f52b_lastvisit=1490347056; UtzD_f52b_ulastactivity=1489737935%7C0; UtzD_f52b_creditnotice=0D0D2D0D0D0D0D0D0D371681; UtzD_f52b_creditbase=0D0D431D0D0D0D0D0D0; UtzD_f52b_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; _gat=1; think_language=zh-CN; ad_index_dialog=1; _ga=GA1.2.714695514.1490350613; yaozh_logintime=1490519522; yaozh_user=385042%09gjpharm; yaozh_userId=385042; db_w_auth=371681%09gjpharm; UtzD_f52b_lastact=1490519524%09uc.php%09; UtzD_f52b_auth=dfc0e77E4QPMxa3wJlU%2Bme25%2BoK4ddYyXNEWDqZrqghB1z%2FI%2FeBbzv%2BjJ3tjistgw1d2YVH1iwxCjirv30tMomkXAk4; zbpreid=; _ga=GA1.3.714695514.1490350613; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1490350613; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1490523034; WAF_SESSION_ID=f2f4948b6c718060587d3b3f87106232'}
# 测试数据已经ok
# data = [
#     {"com": "恒瑞医药", "pro": "多西他赛"},# 170条
#     {"com": "恒瑞医药", "pro": "奥沙利铂"},# 194条
#     {"com": "恒瑞医药", "pro": "厄贝沙坦"},# 104条
# ]
# data = [
#     # {"com":"恒瑞医药","pro":"伊立替康"},
#     # {"com":"恒瑞医药","pro":"来曲唑"},
#     # {"com":"恒瑞医药","pro":"亚叶酸钙"},
#     # {"com":"恒瑞医药","pro":"七氟烷"},
#     # {"com":"恒瑞医药","pro":"碘佛醇"},
#     # {"com":"恒瑞医药","pro":"右美托咪定"},
#     # {"com":"恒瑞医药","pro":"苯磺顺阿曲库铵"},
#     {"com":"恩华药业","pro":"咪达唑仑"},
#     {"com":"恩华药业","pro":"瑞芬太尼"},
#     {"com":"恩华药业","pro":"依托咪酯"},
#     {"com":"恩华药业","pro":"丙泊酚"},
#     {"com":"恩华药业","pro":"右美托咪定"},
#     {"com":"恩华药业","pro":"利培酮"},
#     {"com":"恩华药业","pro":"齐拉西酮"},
#     {"com":"恩华药业","pro":"阿立哌唑"},
#     {"com":"恩华药业","pro":"丁螺环酮"},
#     {"com":"恩华药业","pro":"度洛西汀"},
# ]
# data = [
#     {"com":"华东制药","pro":"阿卡波糖"},
#     {"com":"华东制药","pro":"泮托拉唑"},
#     {"com":"华东制药","pro":"吗替麦考酚酯"},
#     {"com":"华东制药","pro":"二甲双胍"},
#     {"com":"华东制药","pro":"吡格列酮"},
#     {"com":"华东制药","pro":"他克莫司"},
#     {"com":"华东制药","pro":"百令胶囊"},
#     {"com":"信立泰","pro":"氯吡格雷"},
#     {"com":"信立泰","pro":"头孢呋辛"},
#     {"com":"信立泰","pro":"头孢吡肟"},
#     {"com":"信立泰","pro":"头孢西丁"},
#     {"com":"信立泰","pro":"贝那普利"},
#     {"com":"人福","pro":"芬太尼"},
#     {"com":"人福","pro":"瑞芬太尼"},
#     {"com":"人福","pro":"舒芬太尼"},
#     {"com":"人福","pro":"纳布非"},
#     {"com":"人福","pro":"氢吗啡酮"},
#     {"com":"海正药业","pro":"表柔比星"},
#     {"com":"海正药业","pro":"美罗培南"},
#     {"com":"海正药业","pro":"氨基葡萄糖"},
#     {"com":"海正药业","pro":"异帕米星"},
#     {"com":"海正药业","pro":"亚胺培南"},
#     {"com":"海正药业","pro":"腺苷蛋氨酸"},
#     {"com":"海正药业","pro":"重组人II型肿瘤坏死因子受体"},
#     {"com":"天士力","pro":"复方丹参滴丸"},
#     {"com":"天士力","pro":"替莫唑胺"},
#     {"com":"天士力","pro":"重组人尿激酶"},
#     {"com":"天士力","pro":"益气复脉"},
#     {"com":"天士力","pro":"注射用丹参多酚酸"},
#     {"com":"益佰制药","pro":"艾迪注射液"},
#     {"com":"益佰制药","pro":"复方斑蝥胶囊"},
#     {"com":"双鹭药业","pro":"复合辅酶"},
#     {"com":"双鹭药业","pro":"胸腺五肽"},
#     {"com":"双鹭药业","pro":"白细胞介素-2"},
#     {"com":"双鹭药业","pro":"注射用重组人白介素-11"},
#     {"com":"翰宇药业","pro":"胸腺五肽"},
#     {"com":"翰宇药业","pro":"特利加压素"},
#     {"com":"翰宇药业","pro":"去氨加压素"},
#     {"com":"翰宇药业","pro":"生长抑素"},
#     {"com":"舒泰神","pro":"鼠神经生长因子"},
#     {"com":"舒泰神","pro":"聚乙二醇+电解质，复方"},
#     {"com":"丽珠","pro":"参芪扶正"},
#     {"com":"丽珠","pro":"尿促卵泡素"},
#     {"com":"丽珠","pro":"亮丙瑞林"},
#     {"com":"丽珠","pro":"鼠神经生长因子"},
#     {"com":"丽珠","pro":"艾普拉唑"},
# ]
data = [
    {"com":"通化东宝","pro":"重组人胰岛素",},
    {"com":"仙琚制药","pro":"黄体酮",},
    {"com":"仙琚制药","pro":"米非司酮",},
    {"com":"仙琚制药","pro":"米非司酮/米索前列醇",},
    {"com":"仙琚制药","pro":"维库溴铵",},
    {"com":"仙琚制药","pro":"罗库溴铵",},
    {"com":"北陆药业","pro":"碘海醇",},
    {"com":"北陆药业","pro":"碘克沙醇",},
    {"com":"北陆药业","pro":"钆喷酸葡胺",},
    {"com":"北陆药业","pro":"碘帕醇",},
    {"com":"北陆药业","pro":"九味镇心",},
    {"com":"海思科","pro":"多拉司琼",},
    {"com":"海思科","pro":"纳美芬"},
    {"com":"海思科","pro":"脂肪乳"},
    {"com":"海思科","pro":"复方氨基酸注射液(18AA-Ⅶ)"},
    {"com":"京新药业","pro":"瑞舒伐他汀",},
    {"com":"京新药业","pro":"辛伐他汀",},
    {"com":"京新药业","pro":"舍曲林",},
    {"com":"京新药业","pro":"地衣芽孢杆菌",},
    {"com":"广生堂","pro":"拉米夫定",},
    {"com":"广生堂","pro":"阿德福韦酯",},
    {"com":"广生堂","pro":"恩替卡韦",},
    {"com":"红日药业","pro":"血必净",},
    {"com":"红日药业","pro":"法舒地尔",},
    {"com":"红日药业","pro":"低分子肝素钙",},
    {"com":"常山","pro":"低分子量肝素钙",},
    {"com":"常山药业","pro":"达肝素钠",},
    {"com":"四川科伦","pro":"碳酸氢钠",},
    {"com":"四川科伦","pro":"丙氨酰谷氨酰胺",},
    {"com":"四川科伦","pro":"复方氨基酸"},
    {"com":"四川科伦","pro":"复方氯化钠"},
    {"com":"四川科伦","pro":"葡萄糖氯化钠",},
    {"com":"四川科伦","pro":"葡萄糖",},
    {"com":"双鹤药业","pro":"葡萄糖氯化钠",},
    {"com":"双鹤药业","pro":"氯化钠",},
    {"com":"双鹤药业","pro":"复方氯化钠"},
    {"com":"双鹤药业","pro":"葡萄糖",},
    {"com":"双鹤药业","pro":"格列喹酮",},
    {"com":"双鹤药业","pro":"匹伐他汀",},
    {"com":"健康元","pro":"美罗培南",},
    {"com":"健康元","pro":"氨曲南",},
    {"com":"誉衡药业","pro":"鹿瓜多肽",},
    {"com":"尔康","pro":"磺苄西林",},
    {"com":"石药集团","pro":"丁苯酞",},
    {"com":"三生制药","pro":"重组人白介素-2",},
    {"com":"三生制药","pro":"重组人促红素(CHO细胞)"},
    {"com":"三生制药","pro":"重组人干扰素α",},
    {"com":"三生制药","pro":"重组人血小板生成素",},
    {"com":"乐普","pro":"氯吡格雷",},

]
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'MEIQIA_EXTRA_TRACK_ID=0070956c107b11e7a7c00246fd076266; PHPSESSID=ugmp68m7sapkupis94k648lrf1; ad_index_dialog=1; WAF_SESSION_ID=d0dd266e8c116a8a07fd70f72b2a7b7a; think_language=zh-CN; UtzD_f52b_saltkey=U2HR3HHx; UtzD_f52b_lastvisit=1491560891; WAF_SESSION_ID=4979de45699082aa58b7853719cbd2e0; UtzD_f52b_ulastactivity=1489737935%7C0; _gat=1; yaozh_logintime=1491567363; yaozh_user=385042%09gjpharm; yaozh_userId=385042; db_w_auth=371681%09gjpharm; UtzD_f52b_lastact=1491567364%09uc.php%09; UtzD_f52b_auth=02642mFxI8VsowF%2B0l%2F7%2FUXgb4rIZ1R0a2mtEvj2r%2BEHQpXbkzZ4EPAU%2FAs%2FT%2BoZQ7lEcqWc47ZTaAmkV98wPVCCT08; _ga=GA1.2.714695514.1490350613; _ga=GA1.3.714695514.1490350613; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1490350613%2C1491564485; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1491567384; zbpreid=',
    'Host':'db.yaozh.com',
    'Referer':'https://db.yaozh.com/yaopinzhongbiao',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}
def get_db():
    db = pymysql.connect(host='202.112.113.203',
                         user='sxw',
                         passwd='0845',
                         db='sns',
                         port=3306,
                         charset='utf8')
    return db


def get_url():

    db = get_db()
    cursor = db.cursor()
    sql = "select * from url"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if len(rows) > 0:
        return
    print("get url")
    for d in data:
        zb_shengchanqiye = d["com"]
        yname = d["pro"]
        url = urls.format(yname, zb_shengchanqiye, first, p)
        try:
            proxies = get_ip()
            code = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False).status_code
            if proxies and code == 200:
                response = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False)
                tree = html.fromstring(response.text)
                total = tree.xpath('//div[@class="tr offset-top"]/@data-total')[0]
                print("total:\n")
                print(total)
                page = int(int(total) / 20) + 1
                print("page:\n")
                print(page)

                for j in range(1, page + 1):
                    urltmp = re.subn('p=\d+', 'p=' + str(j), url)[0]
                    print(urltmp)
                    # utf8string = urltmp.encode('utf-8')
                    # print(utf8string)
                    sql = "insert into url(url, times) values('{0}', '0')".format(urltmp)
                    print(sql)
                    cursor.execute(sql)
                    db.commit()
        except Exception as e:
            print(yname, zb_shengchanqiye + "have no result.")
            f = open('noresult.txt', 'a')
            f.write(yname + zb_shengchanqiye + "have no result.")
            f.close()
            continue
    db.close()


def get_data():
    db = get_db()
    cursor = db.cursor()
    start_sql = "select url from url where times = '0'"
    cursor.execute(start_sql)
    data = cursor.fetchall()

    while len(data) != 0:

        for u in data:
            flag = False
            time.sleep(5)
            try:
                proxies = get_ip()
                # proxies = {'https': 'https://127.0.0.1:80', 'http': 'http://127.0.0.1:80'}
                code = requests.get(u[0], headers=headers, proxies=proxies, allow_redirects=False).status_code
                if proxies and code == 200:
                    print("success!")
                    response = requests.get(u[0], headers=headers, proxies=proxies, allow_redirects=False)
                    print(response.text)
                    tree = html.fromstring(response.text)
                else:
                    continue
            except Exception as e:
                print(e)
                print(u[0])
                continue


            tr_len=len(tree.xpath('//tbody/tr'))
            for tr in tree.xpath('//tbody/tr'):
                general_name = name = type = scale = rate = danwei = price = quality = pro_com = tou_com = province = date = beizhu = file = file_link = product = ''
                try:
                    general_name = tr.xpath('td[2]/span/text()')[0]
                except IndexError as e:
                    print(e)
                # print("error")
                #     continue
                try:
                    name = tr.xpath('td[3]/text()')[0]
                except IndexError as e:
                    print(e)
                    # print("error")
                    # continue
                try:
                    type = tr.xpath('td[4]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    scale = tr.xpath('td[5]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    rate = tr.xpath('td[6]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    danwei = tr.xpath('td[7]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    price = tr.xpath('td[8]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    quality = tr.xpath('td[9]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    pro_com = tr.xpath('td[10]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    tou_com = tr.xpath('td[11]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    province = tr.xpath('td[12]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    date = tr.xpath('td[13]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    beizhu = tr.xpath('td[14]/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    file = tr.xpath('td[15]/a/text()')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    file_link = tr.xpath('td[15]/a/@href')[0]
                except IndexError as e:
                    print(e)
                    # continue
                try:
                    product = tr.xpath('td[16]/a/@href')[0]
                except IndexError as e:
                    print(e)
                    # continue
                print(general_name, name, type, scale, rate, danwei, price, quality, pro_com, tou_com, province, date, beizhu, file, file_link, product)

                url = u[0]
                pattern = re.compile(r".*name=(.*)&zb_shengchanqiye=(.*)&first")
                match = re.match(pattern, url).groups()
                kw1 = match[0]
                kw2 = match[1]

                sql = "insert into yzdata(kw1, kw2, general_name, name, type, scale, rate, danwei, price, quality, pro_com, tou_com, " \
                  "province, date, beizhu, file, filelink, product, url) \
                  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                params = (kw1, kw2, general_name, name, type, scale, rate, danwei, price, quality, pro_com, tou_com, province, date, beizhu, file, file_link, product, url)
                # print(params)
                try:
                    cursor.execute(sql, params)
                    db.commit()
                    flag = True
                except Exception as e:
                    print(e)
                    continue
            print("one link over")
            if flag:
                new_sql = "update url set times = '1' where url = '{0}'".format(u[0])
                cursor.execute(new_sql)
                db.commit()
        cursor.execute(start_sql)
        data = cursor.fetchall()
    db.close()


def truncate_table(table):
    db = get_db()
    cursor = db.cursor()
    sql = "truncate table {0}".format(table)
    cursor.execute(sql)
    db.commit()
    db.close()


def test_sql():
    db = get_db()
    cursor = db.cursor()
    start_sql = "select url from url where times = '0'"
    cursor.execute(start_sql)
    data = cursor.fetchall()
    print(data)


def get_ip():
    import json
    r = requests.get('http://127.0.0.1:8000')
    ip_ports = json.loads(r.text)
    # print(ip_ports)
    # ip = ip_ports[0][0]
    # port = ip_ports[0][1]
    for address in ip_ports:
        ip = address[0]
        port = address[1]
        proxies = {'https': 'https://%s:%s' % (ip, port), 'http': 'http://%s:%s' % (ip, port)}
    # proxies = {'https': 'https://%s:%s' % (ip, port)}
    # return proxies
    # if proxies:
    #     return proxies
    # return None
    # print(proxies)
    #     return proxies

        try:
            code = requests.get('https://db.yaozh.com/yaopinzhongbiao', proxies=proxies, allow_redirects=False).status_code
            # r.encoding = 'utf-8'
            # print(code)

        except Exception as e:
            # print(e)
            continue
        if code == 200:
            print(proxies)
            print("get proxies...")
            return proxies
        return None
    return None

if __name__ == '__main__':
    # truncate_table('url')
    # truncate_table('yzdata')
    # get_url()
    get_data()
    # # test_sql()
    # get_ip()
