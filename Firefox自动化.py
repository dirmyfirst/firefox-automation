from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image,ImageEnhance
import pytesseract
import time
import os

#开始打开网页
def log_start():
    url = "https://nqi.gmcc.net:20443/cas/login?service=http%3A%2F%2Fnqi.gmcc.net%3A8090%2Fpro-portal%2Fstruts%2Fportal%2Findex.html#/"
    global driver
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)
    global rep
    rep={'O':'0','I':'1','L':'1','Z':'2','S':'8','&':'8','$':'8'}; 

#获取验证码图片
def get_image():
    driver.get_screenshot_as_file('test1.png')
    location = driver.find_element_by_class_name('vcode-img').location
    size = driver.find_element_by_class_name('vcode-img').size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    test = Image.open("test1.png")
    im = test.crop((left,top,right,bottom))
    im.save('test2.png')
    os.remove('test1.png')

#获取验证码数字
def get_vcode():
    get_image()
    image = Image.open("test2.png")
    image = image.convert('L')
    image = ImageEnhance.Contrast(image)
    image = image.enhance(2.0)
    image.save('test3.png')
    os.remove('test2.png')
    vcode = pytesseract.image_to_string(image)
    for r in rep:
        vcode = vcode.replace(r,rep[r])
    vcode = vcode.split(' ')
    new_vcode = ''.join(vcode)
    os.remove('test3.png')
    return new_vcode

#输入帐号密码验证码登录
def login(username,password):
    double_c = driver.find_element_by_id("username")
    ActionChains(driver).double_click(double_c).perform()
    driver.find_element_by_id("username").send_keys(username)
    time.sleep(1)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(1)
    driver.find_element_by_id("j_captcha_response").send_keys(get_vcode())
    time.sleep(1)
    driver.find_element_by_xpath("//input[@class='btn-submit']").click()

#开始执行
def begin():
    for user_name,pass_word in login_name.items():
        login(user_name,pass_word)
        if mes_error() == True:
            #driver.implicitly_wait(30) #它的用法应该比time.sleep() 更智能，后者只能选择一个固定的时间的等待，前者可以在一个时间范围内智能的等待。
            time.sleep(10)  #进入主页面停留时间，网速慢要将时间调长
            driver.find_element_by_xpath("//a[@class='dis_border']").click()
            time.sleep(5)
        else:
            print("\n验证码输入不正确，将重新开始")

#判断验证码是否正确            
def mes_error():
    try:
        driver.find_element_by_xpath("//div[contains(text(),'验证码有误！')]")
        time.sleep(3)
        return False
    except:  
        print ("\n****验证码输入正确****")
        return True

#主程序                
if __name__ == '__main__':
    login_name = {'test':'test'}
    log_start()
    #执行外部循环
    for i in range(1,6):
        print(f"\n这是正在执行外部循环第{i}次...")
        #执行内部循环
        for j in range(1,5):
            print(f"\n正在执行内部循环第{j}次...")
            begin()
    driver.quit()

