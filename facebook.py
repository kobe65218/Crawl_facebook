import json

from selenium import webdriver
import time
from  bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import numpy as np
from urllib.parse import unquote
import re
caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL' ,
                        'brower':'ALL'}

caps['perfLoggingPrefs'] = {
    'enableNetwork':True,
    'enablePage' : False,
    'enableTimeline':False
}
option =  webdriver.ChromeOptions()
# option.add_argument('--no-sandbox')
# option.add_argument('--headless')
# option.add_argument("--disable-extensions")
# option.add_argument("--allow-running-insecure-content")
# option.add_argument("--ignore-certificate-errors")
# option.add_argument("--disable-single-click-autofill")
# option.add_argument("--disable-autofill-keyboard-accessory-view[8]")
# option.add_argument("--disable-full-form-autofill-ios")
option.add_experimental_option('w3c', False)
prefs = {
        'profile.default_content_setting_values': {
            'images': 1,
            'permissions.default.stylesheet':2,
            'javascript': 1
        }
    }

option.add_experimental_option("prefs",prefs)
option.add_experimental_option('perfLoggingPrefs', {
    'enableNetwork':True,
    'enablePage' : False
})
# option.add_argument("ignore-certificate-errors")
option.add_argument("--disable-notifications")
driver = webdriver.Chrome(desired_capabilities=caps, options=option)
driver .get('https://www.facebook.com/?stype=lo&jlou=AffaQOipEw6f7To3BhArLIJBajOrBGoRMAQ7Bhzr4aaYsWjPSY6XSMLdL2Vq-ltT5BPjFtQW2zcm8NMlF0TX29S2u8ftj9ofnleppVZntmuFwA&smuh=15818&lh=Ac8DARqZTrATBAVV17I')
driver.find_element_by_css_selector("input#email").send_keys("shine655218@gmail.com")
driver.find_element_by_css_selector("input#pass").send_keys("kobe910018")
driver.find_element_by_css_selector("button[name='login']").click()
time.sleep(3)

driver.get("https://www.facebook.com/craziejulia")  #https://www.facebook.com/friends/suggestions/?profile_id=100000160215580
# time.sleep(5)

datas = []
div = 0
last_p = 0
while True:
    count = 0
    #紀錄滾動前高度
    height_before = driver.execute_script(f"return document.body.scrollHeight ;")
    driver.execute_script(f"window.scrollTo(0, {int(height_before) - div});")
    time.sleep(1)
    div += 1000
    # posts_ = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    def log_filter(log_):
        return (
                log_["method"] == "Network.requestWillBeSent" or
                log_["method"] == "Network.request"

        )

    for log in filter(log_filter, logs):
        resp_url = log["params"]["request"]["url"]
        if resp_url == "https://www.facebook.com/ajax/bulk-route-definitions/" : #https://www.facebook.com/ajax/bulk-route-definitions/

            post = log["params"]["request"]["postData"]
            post = np.array(post.split("&"))
            fetch = [ "route_urls" in i  for  i in  post]
            post_fetch = post[fetch]
            data = ["https://www.facebook.com" + unquote(re.match("route_urls\[\d*\]=(.*)",i).groups()[0]) for i in post_fetch]
            datas  += data
            print(data)
            posts = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
            posts_len = len(posts)
            last_post = posts_len
            count  += 1
            print("network post")
            while True:
                posts_now = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                posts_len_now = len(posts_now)
                print("post前po文數：", last_p, "post後po文數：", posts_len_now)

                # 如果post後大於等於post前 代表已經loading完
                if posts_len_now >= last_p:
                    break



    posts_now = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
    posts_len_now = len(posts_now)
    # 紀錄post前貼文數
    last_p = posts_len_now

    time.sleep(1)
    heigh_after = driver.execute_script(f"return document.body.scrollHeight ;")
    print("滑動後高度：" , heigh_after,  "滑動前高度：" , height_before)

    # 如果高度都沒變及post數為0代表已經滑到底
    if height_before == heigh_after and count == 0:
        break


#%%


import requests
filter_data = ["599383947142230" in i for i in datas]
datas = np.array(datas)
filter_data = datas[filter_data]

print(filter_data)

#%%
for i in filter_data:
    html = requests.get(i)
    soup =BeautifulSoup(html.text, "lxml")
    dd = soup.select("div.gtad4xkn")
    print(dd)





#%%

#%%
import re
comments = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")

for index , comment in enumerate(comments):
        # comment.find_element_by_css_selector("div div > div > div > div > div.pybr56ya.dati1w0a.hv4rvrfc.n851cfcs.btwxx1t3.j83agx80.ll8tlv6m")
        print(index)
        # print(comment.text)
        test = comment.find_element_by_css_selector("span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.hrzyx87i.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain")
        print(test.text)
        count = 0
        #
        # try:
        #     test[-1].click()
        # except:
        #     pass

        # if re.match("檢視另\d*則留言" , test[-1].text) != None:
        #         test[-1].click()


#%%
from bs4 import  BeautifulSoup

soup = BeautifulSoup(driver.page_source , "lxml")
posts = soup.select("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")

for index , post in enumerate(posts):
    print(index)
    comment = post.select("div.gtad4xkn")
    for i in comment[0]:
        print(i.text)
