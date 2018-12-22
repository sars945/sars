import re
import socket
import struct
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import pymysql
url = 'http://api.xiaojie666.com/xiaojie/credit/query.do?nickName=炮兵sars'
try:
    credit = requests.get(url)
    credit.encoding = 'utf-8'
    CREDIT = credit.text
    pattern = '"credit":(.*?),"'
    CREDIT = re.findall(pattern, CREDIT)
    Credit = int(CREDIT[0])
    Credit = int(Credit/1000)
except:
    con = pymysql.connect(host='localhost', user='root', passwd='Sars@945945', charset='utf8')
    cur = con.cursor()
    cur.execute('use xiaojie')
    sql_insert = 'select * from xiaojie order by time desc limit 1'
    cur.execute(sql_insert)
    data_one = cur.fetchone()
    Credit = data_one[1]
    Credit = int(Credit/1000)
driverOptions = webdriver.ChromeOptions()
driverOptions.add_argument(r"user-data-dir=C:\Users\86185\AppData\Local\Google\Chrome\User Data")
#driverOptions.add_argument('-headless')
driver = webdriver.Chrome(options=driverOptions)
driver.get('https://www.douyu.com/74751')
driver.maximize_window()
sk_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
sk_client.connect((host,port))
js = 'document.getElementsByClassName("ZoomTip-tipClose")[0].click()'
time.sleep(1)
try:
    driver.execute_script(js)
except:
    print('')
def send_msg(msg):
    content = msg.encode()
    length = len(content) + 8
    code = 689
    head = struct.pack('i', length) + struct.pack('i', length) + struct.pack('i', code)
    try:
        sk_client.sendall(head + content)
    except:
        time.sleep(2)
def init():
    msg_login = 'type@=loginreq/roomid@=74751/\x00'
    send_msg(msg_login)
    time.sleep(1)
    msg_join = 'type@=joingroup/rid@=74751/gid@=-9999/\x00'
    send_msg(msg_join)
def get_dm():
    pattern = re.compile(b'type@=chatmsg/.+?/nn@=(.+?)/txt@=(.+?)/.+?/level@=(.+?)/')
    s1 = 0
    s2 = 0
    s3 = 0
    join = 0
    xx = 0
    ci = 0
    while True:
        buffer = b''
        if driver.current_url != 'https://www.douyu.com/74751':
            driver.get('https://www.douyu.com/74751')
        while True:
            try:
                recv_data = sk_client.recv(4096)
                buffer += recv_data
            except:
                time.sleep(2)
            if recv_data.endswith(b'\x00'):
                break
        for nn, txt, level in pattern.findall(buffer):
            try:
                #print("[lv.{:0<2}][{}]: {}".format(level.decode(), nn.decode(), txt.decode().strip()))
                if nn.decode() == '炮兵sars':
                    print(txt.decode().strip())
                min = time.strftime('%M', time.localtime())
                sec = time.strftime('%S', time.localtime())
                if '9' in sec:
                    s3 = 0
                    s1 = 0
                    s2 = 0
                if '#1' in txt.decode().strip() and '0' in txt.decode().strip():
                    s1 += 1
                    s3 += 1
                if '#2' in txt.decode().strip() and '0' in txt.decode().strip():
                    s2 += 1
                    s3 += 1
                if s3 == 20:
                    if ci<1:
                        if s1 > s2:
                            s1 = (s1 - s2)
                            yafen = s1*Credit*15
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").clear()
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys('#1 ', yafen)
                            time.sleep(1)
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys(Keys.ENTER)
                            time.sleep(9)
                            ci = ci+1
                        elif s1 < s2:
                            s2 = (s2 - s1)
                            yafen = s2*Credit*10
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").clear()
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys('#2 ', yafen)
                            time.sleep(1)
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys(Keys.ENTER)
                            time.sleep(9)
                            ci = ci + 1
                if '#入团' in txt.decode().strip():
                    join += 1
                    if join == 10:
                        driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").clear()
                        driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys('#入团 ')
                        time.sleep(1)
                        driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys(Keys.ENTER)
                        time.sleep(9)
                if '#抢分' in txt.decode().strip():
                    xx += 1
                    if xx == 15:
                        for i in range(0,3):
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").clear()
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys('#抢分 ',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                            time.sleep(1)
                            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys(Keys.ENTER)
                            time.sleep(9)
                if '9' in min:
                    now = int(sec)
                    if now < 1:
                        join = 0
                        xx = 0
                        ci = 0
                        time.sleep(1)
            except UnicodeDecodeError as e:
                print(e)
def keep_live():
    while True:
        time.sleep(15)
        msg_keep = 'type@=mrkl/\x00'
        send_msg(msg_keep)
def sign():
    m = 0
    while 1:
        try:
            driver.find_element_by_xpath("//div[@class='ChatSend-button ']").click()
        except:
            time.sleep(20)
            try:
                driver.find_element_by_xpath("//div[@class='ChatSend-button ']").click()
            except:
                driver.refresh()
                time.sleep(2)
                js = 'document.getElementsByClassName("ZoomTip-tipClose")[0].click()'
                driver.execute_script(js)
        time1 = time.strftime('%M', time.localtime())
        time2 = time.strftime('%H', time.localtime())
        if time2 == '12':
            if time1 == '05':
                driver.refresh()
        if time1 == '00':
            try:
                driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").clear()
                driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys('#签到 ', m)
                time.sleep(1)
                driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys(Keys.ENTER)
                time.sleep(9)
            except:
                driver.refresh()
            m = m+1
        if time1 == '30':
            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").clear()
            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys('#签到 ', m)
            time.sleep(1)
            driver.find_element_by_xpath("//textarea[@class='ChatSend-txt']").send_keys(Keys.ENTER)
            time.sleep(9)
            m = m+1
        time.sleep(50)
def point():
    con = pymysql.connect(host='localhost', user='root', passwd='Sars@945945', charset='utf8')
    cur = con.cursor()
    cur.execute('use xiaojie')
    sql_insert = 'select * from xiaojie order by time desc limit 1'
    cur.execute(sql_insert)
    data_one = cur.fetchone()
    old_point = data_one[1]
    while 1:
        try:
            jifen = requests.get(url)
            jifen.encoding = 'utf-8'
            JIFEN = jifen.text
            pattern = '"credit":(.*?),"'
            Jifen = re.findall(pattern, JIFEN)
            point = int(Jifen[0])
        except:
            print('服务器繁忙')
        if point != old_point:
            differential = point - old_point
            sql_insert  = 'insert into xiaojie(time,point,difference) values (%s,%s,%s);'
            DATA = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            DATA = str(DATA)
            POINT = point
            DIFFERENCE = differential
            cur.execute(sql_insert, [DATA, POINT, DIFFERENCE])
            con.commit()
            old_point = point
            print(old_point)
        time.sleep(60)
def main():
    init()
    t1 = Thread(target=get_dm)
    t2 = Thread(target=keep_live)
    t3 = Thread(target=sign)
    t4 = Thread(target=point)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
if __name__ == '__main__':
    main()