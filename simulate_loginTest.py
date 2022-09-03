import time
import os
import re
import  tkinter as tk
import threading
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


flagx=0                                                                                 # 0代表初次使用，1代表已使用过，在本地保有数据
account=''
password=''
message=''                                                                           # 存放获取打卡信息

url="https://cas.dgut.edu.cn/home/Oauth/getToken/appid/yqfkdaka/state/home.html"


# 模拟浏览器打开网站
# driver = webdriver.Chrome()
# driver.get(url)

options=Options()                                                              # 创建Chrome参数对象
options.headless = True                                                     # 设置成可视化无界面模式
driver = webdriver.Chrome(options=options)                   # 创建Chrome无界面对象
driver.get(url)

def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)        # 如果主线程退出，守护线程也会自动退出
    # 守护 !!!
    t.daemon = True
    # 启动线程
    t.start()

# 检测本地是否已保存有登录数据
def is_savedata():
    # 读取文件大小
    if(os.path.exists('data.txt')==True):# 文件存在
        return True
    else:
        return False

# 从本地文件获取登录信息
def get_data():
    global account,password
    list = []
    with open('data.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            list.append(line)
    account = list[0]
    password = list[1]

# 保存数据到本地
def save_data(str1,str2):
    global  account,password
    account = str1
    password = str2
    with open("data.txt","w") as f:
        f.write(account+'\n'+password)

your_temperature='36.5' # 网页要求填保留到一位的小数

# 账号登录界面账号、密码栏、登录按钮控件的id，用于定位
idofaccount='username'
idofpassword='casPassword'
idofloginBtn='loginBtn'

# 温度填写框的定位
nameofTemperature="27"

str="您今天已打卡成功"  # 打卡成功会检测到的字符串
# str_again_submit = "您已撤回今天的打卡"  # 撤回打卡的字符串
# 打卡界面提交按钮的xpath
path_of_submitBtn = "/html[@class=' ']/body/div[@id='app']/div[@class='container']/div[@class='van-tabs van-tabs--card']/div[@class='van-tabs__content van-tabs__content--animated']/div[@class='van-tabs__track']/div[@class='van-tab__pane-wrapper']/div[@class='van-tab__pane']/form[@class='form van-form']/div[@class='van-cell-group van-cell-group--inset van-hairline--top-bottom']/div[@class='van-cell'][2]/div[@class='van-cell__title']/div[@class='van-cell__label']/div/button[@class]"
# 打卡界面的标头的xpath
path_of_dktip="/html[@class=' ']/body/div[@id='app']/div[@class='container']/div[@class='van-tabs van-tabs--card']/div[@class='van-tabs__content van-tabs__content--animated']/div[@class='van-tabs__track']/div[@class='van-tab__pane-wrapper']/div[@class='van-tab__pane']/div[@class='tipbox']/div[@class='van-cell-group van-cell-group--inset van-hairline--top-bottom']/div[@class='van-grid van-hairline--top'][1]/div[@class='van-grid-item']/div[@class='van-grid-item__content van-grid-item__content--center van-hairline']/div[@class='van-grid-item__icon-wrapper']/div"

# 检测第一行信息,返回标志
def detect_dktip():
    # 检测今天是否已经打卡
    title = driver.find_element(By.XPATH, path_of_dktip)
    flag = title.text.find(str)
    return flag

# 模拟登录打卡
def do_login(driver):
    global message
    try:
        # 将窗口最大化
        driver.maximize_window()
        # 找到登录框 输入账号密码
        driver.find_element(By.ID, idofaccount).send_keys(account)
        driver.find_element(By.ID,idofpassword).send_keys(password)
        driver.find_element(By.ID,idofloginBtn).click()
        # 延时
        time.sleep(11)   # 参数与你的网速相关，如果网页没加载完就往后执行，会定位不到元素而报错

        # # 检测今天是否已经打卡
        # title = driver.find_element(By.XPATH, path_of_dktip)
        # flag = title.text.find(str)
        flag=detect_dktip()
        if ( flag != -1):   # 已打卡
            title = driver.find_element(By.XPATH, path_of_dktip)
            day = re.findall("\d+", title.text)[0]  # 获取打卡天数
            message = "今天已打卡,已打卡" + day + "天"

        else:        # 今天未打卡
            button = driver.find_element(By.XPATH,path_of_submitBtn)
            driver.execute_script("arguments[0].click()",button)
            time.sleep(30)                                                          # 校园网测得打卡等待用时23.23秒
            flag = detect_dktip()   # 重新检测第一行

            # 点击提交按钮操作

        # 重新提交今日体温操作
        # i=4 # 3个数字加小数点，要按4次delete
        # while(i>0):
        #     driver.find_element(By.NAME,nameofTemperature).send_keys(Keys.BACK_SPACE)
        #     i=i-1
        # driver.find_element(By.NAME,nameofTemperature).send_keys(your_temperature)

        # 检测是否打卡成功
            if(flag!=-1):
                title = driver.find_element(By.XPATH, path_of_dktip)
                day = re.findall("\d+", title.text)[0]  # 获取打卡天数
                message = "打卡成功,已打卡"+day+"天"
            else:
                message = "出错了，请手动打卡"

    except Exception as e:
        print("出现错误",e)

class TkWindow():    # 初次登录窗口类，用于保存输入的账号密码信息
    def __init__(self):
        self.root = tk.Tk()
        # button2
        # self.button2 = tk.Button(self.root, text='更改登录信息',command=lambda :self.set_data(flagx))
        self.button2 = tk.Button(self.root, text='更改登录信息', command=lambda: thread_it(self.set_data, flagx))
        self.button2.grid(row=3, column=1,sticky=tk.E, padx=30, pady=5)

    # 绘制修改登录信息的界面
    def draw_MessageBox(self):
        # 设置标签信息
        self.label1 = tk.Label(self.root, text='账号：')
        self.label1.grid(row=0, column=0)
        self.label2 = tk.Label(self.root, text='密码：')
        self.label2.grid(row=1, column=0)

        # 存放输入框信息
        self.message1 = tk.StringVar()
        self.message2 = tk.StringVar()

        # 创建输入框
        self.entry1 = tk.Entry(self.root, textvariable=self.message1)
        self.entry1.grid(row=0, column=1, padx=10, pady=5)
        self.entry2 = tk.Entry(self.root, textvariable=self.message2, show='*')  # 将密码用指定的字符来显示
        self.entry2.grid(row=1, column=1, padx=10, pady=5)

        # 下面self.show传参巨坑，python自动转换参数为(self,self.entry1.get(),self.entry2.get())（已更改回调函数)
        # self.button1 = tk.Button(self.root, text='打卡',command=lambda: self.save_datax(self.entry1.get(), self.entry2.get()))
        self.button1 = tk.Button(self.root, text='打卡',
                                 command=lambda: thread_it(self.save_datax,self.entry1.get(),self.entry2.get()))
        self.button1.grid(row=3, column=0, sticky=tk.W, padx=30, pady=5)

    # button2的回调函数
    def set_data(self,flagz):
        if(flagz!=0):    # 修改登录信息
            self.label3.destroy()
            self.button2.grid(row=3, column=1,sticky=tk.E, padx=30, pady=5) # 恢复button2初始布局
        self.draw_MessageBox()


    # 执行打卡操作并显示程序执行获得的打卡信息
    def show_message(self):
        self.label3 = tk.Label(self.root, text=message)
        self.label3.grid(row=0, sticky=W + E)
        self.button2.grid(row=1, sticky=W + E)

    # 打卡
    def sign_in(self):
        do_login(driver)
        self.show_message()
        tk.mainloop()

    # 销毁布局
    def destroy_layout(self):
        self.label1.destroy()
        self.label2.destroy()
        self.entry1.destroy()
        self.entry2.destroy()
        self.button1.destroy()

    # botton1的回调函数
    def save_datax(self,str1, str2):
        global flagx
        flagx =1
        save_data(str1,str2) # 保存登录信息到本地
        self.destroy_layout()
        do_login(driver)  # 登录界面并打卡
        self.show_message()


if __name__=='__main__':
    # 创建交互框对象
    tw = TkWindow()
    if is_savedata() == True:  # 如果文件存在
        flagx = 1
        get_data()
        tw.sign_in()
    else:  # 第一次登录弹出账号密码输入框
        tw.draw_MessageBox()
        tk.mainloop()
    #退出
    driver.quit()


