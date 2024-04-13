import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def switch_new_win():
    driver._switch_to.window(driver.window_handles[-1])

def switch_first_win():
    driver._switch_to.window(driver.window_handles[0])

def wallet_connect():
    ## 切换到钱包弹窗
    switch_new_win()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value='//div[text()="连接"]').click()
    switch_new_win()

def wallet_sign():
    switch_new_win()
    time.sleep(1)
    driver.find_element(by=By.XPATH, value='//div[text()="确认"]').click()
    switch_new_win()
def get_privite_key():
    return '0x0d1489ee59ff8d627b4bcf896a0fd899e68610dc48afa98eec7ea3c4b43d6725'


def get_wallet_password():
    return 'cyx00000!'


driver = None


def import_wallet():
    chroptions = webdriver.ChromeOptions()
    chroptions.add_extension(extension='./test.crx')
    driver = webdriver.Chrome(options=chroptions)
    time.sleep(5)

    driver._switch_to.window(driver.window_handles[1])
    time.sleep(5)
    allButton = driver.find_elements(By.XPATH, '//button')
    allButton[1].click()
    time.sleep(5)

    ## 导入私钥选择
    import_key = driver.find_elements(By.CLASS_NAME, value='_left_kpxtk_39')[1]
    import_key.click()
    privite_key = get_privite_key()
    # 私钥
    time.sleep(5)
    privite_tab = driver.find_element(By.XPATH, '//div[text()="私钥"]')

    privite_tab.click()

    time.sleep(5)
    # 发现私钥的文本域
    privite_text = driver.find_element(By.TAG_NAME, value='textarea')
    privite_text.send_keys(get_privite_key())
    # 点击导入
    time.sleep(10)
    driver.find_elements(by=By.XPATH, value="//button[@type='submit']")[1].click()
    time.sleep(5)
    # 点击确认
    confirm = driver.find_element(by=By.XPATH, value="//button[@type='button']")
    confirm.click()
    time.sleep(5)
    # 设置密码
    password_input_arr = driver.find_elements(By.TAG_NAME, value='input')
    time.sleep(5)
    # 密码
    password_input_arr[0].send_keys(get_wallet_password())
    time.sleep(5)
    # 确认密码
    password_input_arr[1].send_keys(get_wallet_password())
    time.sleep(5)
    # 确认
    driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
    time.sleep(5)
    driver.find_element(by=By.XPATH, value="//button[@type='button']").click()

    time.sleep(5)
    driver.find_elements(by=By.XPATH, value="//button[@type='button']")[2].click()

    time.sleep(10)

    driver.close()
    return driver

def connect_wallet():
    connect_wallet = driver.find_element(By.XPATH, '//button[text()="Connect Wallet"]')
    connect_wallet.click()
    # 点击链接钱包
    ## ok钱包
    time.sleep(5)
    driver.find_element(by=By.XPATH, value='//span[text()="OKXWallet"]').click()
    time.sleep(5)
    # 点击确认
    wallet_connect()
    # 签名
    time.sleep(5)
    try:
        wallet_sign()
    except BaseException:
        print('不需要签到')
    switch_first_win()
    # 点击签到按钮
    driver.find_element(by=By.CLASS_NAME, value='signIn').click()
    time.sleep(5)


driver = import_wallet()
driver._switch_to.window(driver.window_handles[0])
## 猫头鹰
driver.get('https://owlto.finance/?ref=0x498D7e7A6ea02b8f38413aD074c3713e34d767E1')
time.sleep(10)

connect_wallet()
# 链接以后选择网络
index =0
for i in range(10):
    try:
        driver.refresh()
        connect_wallet()
        time.sleep(5)
        # 需要重新链接钱包
        driver.find_element(by=By.XPATH,value="//span[text()='zkSync Era']").click()
        time.sleep(1)
        driver.find_elements(by=By.CLASS_NAME,value="select-div-content-con")[2].click()
        break
    except BaseException:
        pass

time.sleep(1)
# 找到签到按钮点击
for i in range(3):
    try:
        old_len = len(driver.window_handles)
        driver.find_element(by=By.XPATH,value="//div[@class='click']").click()
        time.sleep(1)
        new_len = len(driver.window_handles)
        if new_len != old_len:
            break
    except:
        pass
# 确认
driver.find_element(by=By.XPATH,value='//div[text()="确认"]').click()
time.sleep(1)
driver.close()



