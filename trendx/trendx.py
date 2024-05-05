from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from wallet import OkxWallet
#import concurrent.futures
import time
#import sys
import random
#import threading

def confirm_chrome_extesion(driver):
    print("处理钱包插件弹窗...")
    curWindows = driver.current_window_handle
    for wh in driver.window_handles:
        driver._switch_to.window(wh)
        if "chrome-extension" in driver.current_url:
            driver._switch_to.window(wh)
            break

    approve = driver.find_element(By.XPATH, '//div[text()="连接"]')
    approve.click()

    driver._switch_to.window(curWindows)


def approve(driver):
    print("钱包插件确认...")
    curWindows = driver.current_window_handle
    for wh in driver.window_handles:
        driver._switch_to.window(wh)
        if "chrome-extension" in driver.current_url:
            driver._switch_to.window(wh)
            break
        
    approve = driver.find_elements(By.TAG_NAME, 'button')[1]
    approve.click()
    
    driver._switch_to.window(curWindows)


def do_vote(driver):
    time.sleep(5)
    a_elements = driver.find_elements(By.CSS_SELECTOR, ".projectName")
    a_elements[1].click()

    time.sleep(5)
    up = driver.find_elements(By.CSS_SELECTOR, ".up")
    up[len(up) - 1].click()

    time.sleep(random.randint(5, 8))
    vote = driver.find_element(By.XPATH, '//button[text()="Confirmation"]')
    vote.click()
        
    time.sleep(random.randint(4, 9))
    approve(driver)


cur_like = 0
total_num = 60
def like(driver):
    global cur_like
    if cur_like >= total_num:
        return
    
    try:
        time.sleep(3)
        likes = driver.find_elements(By.CSS_SELECTOR, ".like")
        for like in likes:
            if cur_like >= total_num:
                break
            like.click()
            cur_like += 1
            time.sleep(1)
    except Exception as e:
        print("点赞异常, ", e)


def page_load(driver):
    try:
        driver.get("https://app.trendx.tech/projects")

        time.sleep(5)
        vote = driver.find_element(By.XPATH, '//p[text()="Vote"]')
        # 使用ActionChains类模拟鼠标移动到标签
        actions = ActionChains(driver)
        actions.move_to_element(vote).perform()

        time.sleep(3)
        vote = driver.find_element(By.XPATH, '//p[text()="Not voted"]')
        vote.click()

        time.sleep(3)
        vote = driver.find_element(By.XPATH, '//p[text()="1D"]')
        # 使用ActionChains类模拟鼠标移动到标签
        actions = ActionChains(driver)
        actions.move_to_element(vote).perform()

        time.sleep(1)
        vote = driver.find_element(By.XPATH, '//p[text()="7D"]')
        vote.click()
    except Exception as e:
        print("重新加载页面...")
        time.sleep(3)
        page_load(driver)


private_key = ""
wallet_name = "OkxWallet123"
wallet = OkxWallet(private_key, wallet_name, wallet_name)
driver = wallet.do_import()
driver._switch_to.window(driver.window_handles[0])
driver.maximize_window()
driver.get("https://app.trendx.tech?ic=5K2VCZ")#

time.sleep(8)

check_box = driver.find_element(By.XPATH, "//input[@type='checkbox']")
check_box.click()

time.sleep(1)
button_element = driver.find_element(By.CSS_SELECTOR, "button.MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.closeBtn-0-3-325.size-md.vedao-iv907z")
button_element.click()

time.sleep(5)
ra = driver.find_element(By.XPATH, '//p[text()="Receive Airdrop"]')
ra.click()

time.sleep(5)
ra = driver.find_element(By.XPATH, '//button[text()="Connect wallet"]')
ra.click()

time.sleep(5)

confirm_chrome_extesion(driver)

time.sleep(8)
approve(driver)


time.sleep(8)
page_load(driver)


i = 0
while i < 30:
    print("第[" + str(i + 1) + "]次投票")
    try:
        do_vote(driver)

        like(driver)
    except Exception as e:
        print(e)
        print("投票出错")
        i -= 1
        page_load(driver)
    
    time.sleep(random.randint(1, 3))
    driver.back()
    time.sleep(random.randint(2, 4))
    i += 1  # 手动递增 i


print("脚本执行完毕")
time.sleep(360)
