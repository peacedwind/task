import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import common
def get_privite_key():
    return '0x57fc1bd655e10eef94011097eb3b24f90a3c2435c527ced7f4fb4ebfaac3247c'
def get_wallet_password():
    return 'cyx00000!'

def connect_wallet():
    connect_wallet = driver.find_element(By.XPATH, '//button[text()="Connect Wallet"]')
    connect_wallet.click()
    # 点击链接钱包
    ## ok钱包
    time.sleep(5)
    driver.find_element(by=By.XPATH, value='//span[text()="OKXWallet"]').click()
    time.sleep(5)
    # 点击确认
    common.wallet_connect()
    # 签名
    time.sleep(5)
    try:
        common.wallet_sign()
    except BaseException:
        print('不需要签到')
    common.switch_first_win()
    # 点击签到按钮
    driver.find_element(by=By.CLASS_NAME, value='signIn').click()
    time.sleep(5)


driver = common.import_wallet(get_privite_key(),get_wallet_password())
common.switch_first_win()
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
common.switch_new_win()
for i in range(3):
    try:
        driver.find_element(by=By.XPATH,value='//div[text()="确认"]').click()
    except:
        pass
time.sleep(10)
print('签到完成')
driver.close()



