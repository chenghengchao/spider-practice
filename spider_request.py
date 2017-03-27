# coding:utf-8
import requests
from lxml import html
import re
import pymysql
import os


urls = 'https://db.yaozh.com/yaopinzhongbiao?name={0}&zb_shengchanqiye={1}&first={2}&pageSize=20&p={3}'
first = '全部'
p = '1'

cookies = {'PHPSESSID=169t3qjps2uadhdlu7q6nrl020; MEIQIA_EXTRA_TRACK_ID=0070956c107b11e7a7c00246fd076266; WAF_SESSION_ID=f2e50c98c8ba11854406efcb42a09786; mylogin=1; UtzD_f52b_saltkey=oWr2AyrG; UtzD_f52b_lastvisit=1490347056; UtzD_f52b_ulastactivity=1489737935%7C0; UtzD_f52b_creditnotice=0D0D2D0D0D0D0D0D0D371681; UtzD_f52b_creditbase=0D0D431D0D0D0D0D0D0; UtzD_f52b_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; _gat=1; think_language=zh-CN; ad_index_dialog=1; _ga=GA1.2.714695514.1490350613; yaozh_logintime=1490519522; yaozh_user=385042%09gjpharm; yaozh_userId=385042; db_w_auth=371681%09gjpharm; UtzD_f52b_lastact=1490519524%09uc.php%09; UtzD_f52b_auth=dfc0e77E4QPMxa3wJlU%2Bme25%2BoK4ddYyXNEWDqZrqghB1z%2FI%2FeBbzv%2BjJ3tjistgw1d2YVH1iwxCjirv30tMomkXAk4; zbpreid=; _ga=GA1.3.714695514.1490350613; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1490350613; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1490523034; WAF_SESSION_ID=f2f4948b6c718060587d3b3f87106232'}
data = [
    {"com": "恒瑞医药", "pro": "多西他赛"},# 170条
    {"com": "恒瑞医药", "pro": "奥沙利铂"},# 194条
    {"com": "恒瑞医药", "pro": "厄贝沙坦"},# 104条
]
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'PHPSESSID=169t3qjps2uadhdlu7q6nrl020; MEIQIA_EXTRA_TRACK_ID=0070956c107b11e7a7c00246fd076266; WAF_SESSION_ID=feae85155c9e87f4c0f38567b47c1046; mylogin=1; think_language=zh-CN; WAF_SESSION_ID=ed39d9e7e4d6f7099735ceb7b1259056; UtzD_f52b_saltkey=Vx4l4ZLz; UtzD_f52b_lastvisit=1490607937; _gat=1; yaozh_logintime=1490611550; yaozh_user=385042%09gjpharm; yaozh_userId=385042; db_w_auth=371681%09gjpharm; UtzD_f52b_lastact=1490611551%09uc.php%09; UtzD_f52b_auth=3b58cqNFHw5ifWo5Ff3LQPJiZyOs%2FoMKMrbD2azM61iGs7GHeXltnyPuwyrtivcLUCCf6D2CkKE3wCnFf%2B9gdNZRirE; _ga=GA1.2.714695514.1490350613; ad_index_dialog=1; _ga=GA1.3.714695514.1490350613; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1490350613; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1490611584; zbpreid=',
    'Host':'db.yaozh.com',
    'Referer':'https://db.yaozh.com/yaopinzhongbiao',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
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
    for d in data:
        zb_shengchanqiye = d["com"]
        yname = d["pro"]
        url = urls.format(yname, zb_shengchanqiye, first, p)
        response = requests.get(url, headers=headers)
        # print(response.text)
        tree = html.fromstring(response.text)
        # print(tree)
        total = tree.xpath('//div[@class="tr offset-top"]/@data-total')[0]
        print(total)
        page = int(int(total) / 20) + 1
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
    db.close()


def get_data():
    db = get_db()
    cursor = db.cursor()
    sql = "select url from url where times=0"
    cursor.execute(sql)
    data = cursor.fetchall()

    for u in data:
        flag = False
        response = requests.get(u[0], headers=headers)
        tree = html.fromstring(response.text)
        #name_list=[('general_name',2)]
        #item=dict()
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

            # except IndexError as e:
            #     print(e)
            #     # print("error")
            #     continue






            # try:
            #     general_name = tr.xpath('td[2]/span/text()')[0]
            #     name = tr.xpath('td[3]/text()')[0]
            #     type = tr.xpath('td[4]/text()')[0]
            #     scale = tr.xpath('td[5]/text()')[0]
            #     rate = tr.xpath('td[6]/text()')[0]
            #     danwei = tr.xpath('td[7]/text()')[0]
            #     price = tr.xpath('td[8]/text()')[0]
            #     quality = tr.xpath('td[9]/text()')[0]
            #     pro_com = tr.xpath('td[10]/text()')[0]
            #     tou_com = tr.xpath('td[11]/text()')[0]
            #     province = tr.xpath('td[12]/text()')[0]
            #     date = tr.xpath('td[13]/text()')[0]
            #     beizhu = tr.xpath('td[14]/text()')[0]
            #     file = tr.xpath('td[15]/a/text()')[0]
            #     file_link = tr.xpath('td[15]/a/@href')[0]
            #     product = tr.xpath('td[16]/a/@href')[0]
            #     print(general_name, name, type, scale, rate, danwei, price, quality, pro_com, tou_com, province, date, beizhu, file, file_link, product)
            #
            # except IndexError as e:
            #     print(e)
                # print("error")
                # continue
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
            except:
                print("db error")
                continue
        print("one link over")
        if flag:
            new_sql = "update url set times = '1' where url = '{0}'".format(u[0])
            cursor.execute(new_sql)
            db.commit()
    db.close()


if __name__ == '__main__':
    get_url()
    get_data()






