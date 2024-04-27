import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = None
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


def import_wallet(privite_key, wallet_password):
    global driver
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
    # 私钥
    time.sleep(5)
    privite_tab = driver.find_element(By.XPATH, '//div[text()="私钥"]')

    privite_tab.click()

    time.sleep(5)
    # 发现私钥的文本域
    privite_text = driver.find_element(By.TAG_NAME, value='textarea')
    privite_text.send_keys(privite_key)
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
    password_input_arr[0].send_keys(wallet_password)
    time.sleep(5)
    # 确认密码
    password_input_arr[1].send_keys(wallet_password)
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

