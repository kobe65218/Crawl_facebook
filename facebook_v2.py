import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from  bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL' ,
                        'brower':'ALL'}

caps['perfLoggingPrefs'] = {
    'enableNetwork':True,
    'enablePage' : False,
    'enableTimeline':False
}
option =  webdriver.ChromeOptions()
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
driver.find_element_by_css_selector("input#email").send_keys("kobe655218@gmail.com")
driver.find_element_by_css_selector("input#pass").send_keys("kobe910018")
driver.find_element_by_css_selector("button[name='login']").click()
time.sleep(3)

driver.get("https://www.facebook.com/craziejulia")  #https://www.facebook.com/friends/suggestions/?profile_id=100000160215580


First = True
while True:
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
    # 第一次滾動後等待 loading div.rek2kq2y的出現
    if First :
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.rq0escxv.l9j0dhe7.du4w35lb.qmfd67dx.hpfvmrgz.gile2uim.buofh1pr.g5gj957u.aov4n071.oi9244e8.bi6gxh9e.h676nmdw.aghb5jc5 div.rek2kq2y"))
            )
        except:
            print("finish")
    First = False

    # load 是否出現如果沒有代表滑完
    load= driver.find_elements_by_css_selector("div.rq0escxv.l9j0dhe7.du4w35lb.qmfd67dx.hpfvmrgz.gile2uim.buofh1pr.g5gj957u.aov4n071.oi9244e8.bi6gxh9e.h676nmdw.aghb5jc5 div.rek2kq2y")
    print(len(load))
    if len(load) == 0 :
        print("finish")
        break


driver.execute_script("window.scrollTo(0,0);")
posts = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
count = 0

# 點擊所有流言及文章加載內容
while count <= len(posts) - 1:
    post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
    ActionChains(driver).move_to_element(post[count]).perform()
    print(count)
    # count += 1
    while True :
        try:
            post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
            # print(len(post))
            more = post[count].find_element_by_css_selector("div.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql.ii04i59q div[role=button]")
            ActionChains(driver).move_to_element(more).perform()
            print(more.location)
            driver.execute_script("arguments[0].click();", more)
            time.sleep(0.1)
        except NoSuchElementException :
            try:
                post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                btn_more = post[count].find_element_by_css_selector('span.j83agx80.fv0vnmcu.hpfvmrgz span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.hrzyx87i.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
                ActionChains(driver).move_to_element(btn_more).perform()

                driver.execute_script("arguments[0].click();", btn_more)
                time.sleep(0.1)

            except StaleElementReferenceException :
                try:
                    post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                    btn_more = post[count].find_element_by_css_selector('span.j83agx80.fv0vnmcu.hpfvmrgz span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.hrzyx87i.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
                    ActionChains(driver).move_to_element(btn_more).perform()
                    driver.execute_script("arguments[0].click();", btn_more)
                    time.sleep(0.1)
                except NoSuchElementException:  # 點完所有更多留言按鈕了
                    count += 1
                    break
            except NoSuchElementException:  # 點完所有更多留言按鈕了
                count += 1
                break


#%%
soup = BeautifulSoup(driver.page_source , "lxml")
posts = soup.select("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")

for post in posts:

    # 獲取發文日期
    days = post.select("span[id^='jsc'] span.j1lvzwm4.stjgntxs.ni8dbmo4.q9uorilb.gpro0wi8")
    for day in days:
        data = day.text.replace("=" ,"")
        print("day : " ,data)
    contents = post.select("div.qzhwtbm6.knvmm38d span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.hrzyx87i.jq4qci2q.a3bd9o3v.knj5qynh.oo9gr5id.hzawbc8m")

    # 獲取發文內容
    for content in contents:
        data = content.text.replace("\n","")
        if data == "":
            print("content : ","no word!!")
        else:
            print(data)

    # 獲取留言
    comments = post.select("div.cwj9ozl2.tvmbv18p>ul>li div.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql")
    for comment in comments :
        data = comment.text
        print("comment :" , data)





