import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
from  bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

# setting driver
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


def login(email,password):
    driver.get(
        'https://www.facebook.com/?stype=lo&jlou=AffaQOipEw6f7To3BhArLIJBajOrBGoRMAQ7Bhzr4aaYsWjPSY6XSMLdL2Vq-ltT5BPjFtQW2zcm8NMlF0TX29S2u8ftj9ofnleppVZntmuFwA&smuh=15818&lh=Ac8DARqZTrATBAVV17I')
    driver.find_element_by_css_selector("input#email").send_keys(email)
    driver.find_element_by_css_selector("input#pass").send_keys(password)
    driver.find_element_by_css_selector("button[name='login']").click()
    time.sleep(3)

def get_url(url):
    driver.get(url)  # https://www.facebook.com/friends/suggestions/?profile_id=100000160215580


def scroll():
    div = 0
    last_p = 0
    height_before = 0
    count = 0
    while True:
        time.sleep(0.5)

        # 如果高度都沒變及post數為0代表已經滑到底
        heigh_after = driver.execute_script(f"return document.body.scrollHeight ;")
        print("滑動前高度：", height_before, "滑動後高度：", heigh_after)
        if height_before == heigh_after and count == 0:
            break

        count = 0
        # 紀錄滾動前高度
        height_before = driver.execute_script(f"return document.body.scrollHeight ;")
        driver.execute_script(f"window.scrollTo(0, {int(height_before) - div});")
        div += 1000

        # 滾動到底
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")

        # network log
        logs_raw = driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        def log_filter(log_):
            return (
                    log_["method"] == "Network.requestWillBeSent"
            )

        for log in filter(log_filter, logs):
            resp_url = log["params"]["request"]["url"]

            # 如果有post活動 則去等待post後大於post前
            if resp_url == "https://www.facebook.com/ajax/bulk-route-definitions/":  # https://www.facebook.com/ajax/bulk-route-definitions/
                posts = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                posts_len = len(posts)
                last_post = posts_len
                count = 1
                print("network post")

                # 等待貼文loading
                while True:
                    posts_now = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                    posts_len_now = len(posts_now)
                    print("post前po文數：", last_p, "post後po文數：", posts_len_now)
                    # 如果post後大於post前 代表已經loading完
                    if (posts_len_now - last_p) >= 1:
                        # 紀錄post前貼文數
                        last_p = posts_len_now
                        break
                break

# 點擊所有流言及文章加載內容
def click():
    driver.execute_script("window.scrollTo(0,0);")
    posts = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
    count = 0

    while count <= len(posts) - 1:
        post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
        ActionChains(driver).move_to_element(post[count]).perform()
        while True:
            try:
                post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                # print(len(post))
                more = post[count].find_element_by_css_selector(
                    "div.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql.ii04i59q div[role=button]")
                ActionChains(driver).move_to_element(more).perform()
                driver.execute_script("arguments[0].click();", more)
                time.sleep(0.1)
            except NoSuchElementException:
                try:
                    post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                    btn_more = post[count].find_element_by_css_selector(
                        'span.j83agx80.fv0vnmcu.hpfvmrgz span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.hrzyx87i.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
                    ActionChains(driver).move_to_element(btn_more).perform()

                    driver.execute_script("arguments[0].click();", btn_more)
                    time.sleep(0.1)

                except StaleElementReferenceException:
                    try:
                        post = driver.find_elements_by_css_selector("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
                        btn_more = post[count].find_element_by_css_selector(
                            'span.j83agx80.fv0vnmcu.hpfvmrgz span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.hrzyx87i.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
                        ActionChains(driver).move_to_element(btn_more).perform()
                        driver.execute_script("arguments[0].click();", btn_more)
                        time.sleep(0.1)
                    except NoSuchElementException:  # 點完所有更多留言按鈕了
                        count += 1
                        break
                except NoSuchElementException:  # 點完所有更多留言按鈕了
                    count += 1
                    break



def fetch_data():

    datas = []
    soup = BeautifulSoup(driver.page_source, "lxml")
    posts = soup.select("div.du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0")
    for post in posts:

        d = {}

        # 獲取發文日期
        days = post.select("span[id^='jsc'] span a span")
        data = days[0].text.replace("=", "")
        print("day : ", data)
        d["day"] = data


        # 獲取發文內容
        contents = post.select(
            "div.qzhwtbm6.knvmm38d span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.b0tq1wua.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d9wwppkn.fe6kdd0r.mau55g9w.c8b282yb.hrzyx87i.jq4qci2q.a3bd9o3v.knj5qynh.oo9gr5id.hzawbc8m")
        for context in contents:
            data = context.text.replace("\n", "")
            if data == "":
                d["context"] = data
                print("context : ", "no word!!")
            else:
                d["context"] = data
                print("context : ",data)

        # 獲取留言
        comments = post.select("div.cwj9ozl2.tvmbv18p>ul>li div.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.c1et5uql")
        comment_all = []
        for comment in comments:
            data = comment.text
            print("comment :", data)
            comment_all.append(data)
        d["comments"] = comment_all

        datas.append(d)
    return datas
if __name__ == "__main__":
    login("shine655218@gmail.com" , "kobe910018")
    get_url("https://www.facebook.com/craziejulia")
    scroll()
    time.sleep(5)
    click()
    data = fetch_data()
    print(data)
