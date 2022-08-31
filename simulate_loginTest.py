import time
import re
from selenium import webdriver
from  selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText

# 要手动输入的数据
account=""     # 双引号填入自己的登录账号
password="" # 双引号内填自己的登录密码
url="https://cas.dgut.edu.cn/home/Oauth/getToken/appid/yqfkdaka/state/home.html"
your_temperature='36.5' # 网页要求填保留到一位的小数

# 账号登录界面账号、密码栏、登录按钮控件的id，用于定位
idofaccount='username'
idofpassword='casPassword'
idofloginBtn='loginBtn'

# 温度填写框的定位
nameofTemperature="27"

str="您今天已打卡成功"  # 打卡成功会检测到的字符串
# 打卡界面提交按钮的xpath
path_of_submitBtn = "/html[@class=' ']/body/div[@id='app']/div[@class='container']/div[@class='van-tabs van-tabs--card']/div[@class='van-tabs__content van-tabs__content--animated']/div[@class='van-tabs__track']/div[@class='van-tab__pane-wrapper']/div[@class='van-tab__pane']/form[@class='form van-form']/div[@class='van-cell-group van-cell-group--inset van-hairline--top-bottom']/div[@class='van-cell'][2]/div[@class='van-cell__title']/div[@class='van-cell__label']/div/button[@class]"
# 打卡界面的标头的xpath
path_of_dktip="/html[@class=' ']/body/div[@id='app']/div[@class='container']/div[@class='van-tabs van-tabs--card']/div[@class='van-tabs__content van-tabs__content--animated']/div[@class='van-tabs__track']/div[@class='van-tab__pane-wrapper']/div[@class='van-tab__pane']/div[@class='tipbox']/div[@class='van-cell-group van-cell-group--inset van-hairline--top-bottom']/div[@class='van-grid van-hairline--top'][1]/div[@class='van-grid-item']/div[@class='van-grid-item__content van-grid-item__content--center van-hairline']/div[@class='van-grid-item__icon-wrapper']/div"

# 模拟登录打卡
def do_login(driver):
    try:
        # 将窗口最大化
        driver.maximize_window()
        # 找到登录框 输入账号密码
        driver.find_element(By.ID, idofaccount).send_keys(account)
        driver.find_element(By.ID,idofpassword).send_keys(password)
        driver.find_element(By.ID,idofloginBtn).click()
        # 延时
        time.sleep(8)   # 参数与你的网速相关，如果网页没加载完就往后执行，会定位不到元素而报错

        # 疫情防控打卡界面的信息提交按钮
        # driver.find_element(By.XPATH, path).click()   # 这个点击方式会报错，不能实现效果

        # 网上找的解决办法
        button = driver.find_element(By.XPATH,path_of_submitBtn)
        driver.execute_script("arguments[0].click()",button)    # 点击提交按钮操作

        title=driver.find_element(By.XPATH,path_of_dktip)
        # 重新提交今日体温操作
        # i=4 # 3个数字加小数点，要按4次delete
        # while(i>0):
        #     driver.find_element(By.NAME,nameofTemperature).send_keys(Keys.BACK_SPACE)
        #     i=i-1
        # driver.find_element(By.NAME,nameofTemperature).send_keys(your_temperature)

        # 检测是否打卡成功
        day=re.findall("\d+",title.text)[0]     # 获取打卡天数
        flag=title.text.find(str)
        if(button.text=="撤回重填" or flag!=-1):
            print("打卡成功,已打卡"+day+"天")
        else:
            print("出错了，请手动打卡")
    except Exception as e:
        print("出现错误",e)

if __name__=='__main__':
    # 模拟浏览器打开网站
    driver = webdriver.Chrome()
    driver.get(url)
    # 登录并打卡
    do_login(driver)
    #退出
    driver.quit()


