#-*- coding:utf-8 -*-

#实现了通过selenium 爬取网站所有的信息
from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
import  re
import os
from time import sleep
import requests
#开始执行seleum

def getLink():
    Url = 'https://www.zhihu.com/'

    driver = webdriver.Firefox()
    driver.set_window_position(x=50, y=60)
    driver.set_window_size(width=1366, height=700)
    driver.get(url=Url)
    print('开始爬取...清跳转到登录页面')
    sleep(5)
    driver.find_element_by_css_selector('div.account > input:nth-child(1)').send_keys('用户名')
    driver.find_element_by_css_selector('.verification > input:nth-child(1)').send_keys('密码')
    print('验证码开始输入,并点击登录按钮')
    sleep(10)  # 输入验证码
    print('验证码输入完毕，登录')
    driver.get('https://www.zhihu.com/topic/19563245/followers')  # 跳转到清华大学话题
    sleep(2)
    # 点击更多按钮进行加载
    driver.find_element_by_id('zh-load-more').click()
    print('加载一次')
    jiazai = 0
    try:
        while (driver.find_element_by_id('zh-load-more') and jiazai < 100):
            print('点击加载:' + str(jiazai))
            jiazai = jiazai + 1
            driver.find_element_by_id('zh-load-more').click()
    except:
        print('没有更多了')

    info = driver.find_elements_by_class_name('zm-list-avatar-medium')
    f = open('user.txt', 'w')
    for item in info:
        link = item.get_attribute('href')  # 保存用户的个人链接
        f.write(link + '\n')

        '''
        pa = re.compile('people/(\w*)$')
        try:
            userId=pa.findall(str(link))[0]
        except:
            userId='none'
        img_url=item.find_element_by_css_selector('img').get_attribute('src')
        if img_url!=None: #保存头像
            f=open(os.path.join('./img',userId+'.jpg'),'wb')
            f.write(requests.get(img_url).content)
            f.close()
        '''
        # driver.close()  #关闭浏览器
def saveImg():
    Url = 'https://www.zhihu.com/'

    driver = webdriver.Firefox()
    driver.set_window_position(x=50, y=60)
    driver.set_window_size(width=1366, height=700)
    driver.get(url=Url)
    print('开始爬取...清跳转到登录页面')
    sleep(5)
    driver.find_element_by_css_selector('div.account > input:nth-child(1)').send_keys('用户名')
    driver.find_element_by_css_selector('.verification > input:nth-child(1)').send_keys('密码')
    print('验证码开始输入,并点击登录按钮')
    sleep(10)  # 输入验证码
    print('验证码输入完毕，登录')

    f=open('user.txt','r')
    line=f.readline()
    while line:
        line=line.replace('\n','')
        pa = re.compile('people/(\S*)')
        try:
            userId = pa.findall(str(line))[0]
        except:
            userId = 'none'
        driver.get(line)
        sleep(1)
        img_url=driver.find_element_by_class_name('UserAvatar-inner').get_attribute('src')
        if img_url != None:  # 保存头像
            fg = open(os.path.join('./img', userId + '.jpg'), 'wb')
            fg.write(requests.get(img_url).content)
            fg.close()
        line=f.readline()

    f.close()
if __name__=='__main__':
   #getLink()
    saveImg()
