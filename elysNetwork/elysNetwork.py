from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wallet import KelprWallet
import concurrent.futures
import time
import sys
import random
import threading


def clean_chrome_extension(driver):
    #curWindows = driver.current_window_handle
    for wh in driver.window_handles:
        driver._switch_to.window(wh)
        if "chrome-extension" in driver.current_url:
            driver.close()
            break

    driver._switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
    

def confirm_chrome_extesion(driver):
    print("处理钱包插件弹窗...")
    curWindows = driver.current_window_handle
    for wh in driver.window_handles:
        driver._switch_to.window(wh)
        if "chrome-extension" in driver.current_url:
            driver._switch_to.window(wh)
            break

    approve = driver.find_element(By.TAG_NAME, 'button')
    approve.click()

    driver._switch_to.window(curWindows)


def approve(driver):
    print("交易确认...")
    curWindows = driver.current_window_handle
    for wh in driver.window_handles:
        driver._switch_to.window(wh)
        if "chrome-extension" in driver.current_url:
            driver._switch_to.window(wh)
            break
        
    approve = driver.find_elements(By.TAG_NAME, 'button')[1]
    approve.click()
    
    driver._switch_to.window(curWindows)


def claim_deposit(driver):
    print("开始领取测试币")
    try:   
        deposit = driver.find_element(By.XPATH, '//button[text()="Deposit"]')
        deposit.click()

        time.sleep(2)
        
        deposit = driver.find_element(By.XPATH, '//a[text()="Claim Testnet Tokens"]')
        deposit.click()

        time.sleep(3)
        claim = driver.find_element(By.XPATH, '//button[text()="Claim Tokens"]')
        claim.click()

        time.sleep(random.randint(25, 30)) #等待领取完成
    except Exception as e:
        print("领取失败, 准备重试")
        time.sleep(1)
        claim_deposit(driver)

    #claim = driver.find_elements(By.XPATH, '//button[text()="Claim Tokens"]')
    #if (len(claim)) == 1:
        #driver.refresh()
        #claim_deposit()


def swap(driver):
    try:
        js='window.open("https://testnet.elys.network/swap#ELYS/USDC");'

        driver.execute_script(js)

        usdc = '0.003'
        print("swap任务, 交易ELYS: " + usdc)

        time.sleep(random.randint(8, 15))
        
        driver.switch_to.window(driver.window_handles[1])
        
        balance = driver.find_elements(By.XPATH, '//span[text()="0"]')
        if (len(balance) == 2):
            return -1

        time.sleep(random.randint(8, 15))
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        time.sleep(1)
        inputs[0].send_keys(usdc)

        time.sleep(5)
        receive = driver.find_element(By.XPATH, '//button[text()="Receive USDC"]')
        receive.click()

        time.sleep(random.randint(10, 16))
        approve(driver)
        return 0
    except Exception as e:
        print(e)
        print("交易时网络异常, 重新执行")
        clean_chrome_extension(driver)
        if len(driver.window_handles) > 0:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)
        return swap(driver)

def stake(driver):
    try:   
        driver.get("https://testnet.elys.network/earn/staking")

        time.sleep(5)

        elys = '0.001'
        print("质押Elys, 数量: " + elys)
        
        manageButton = driver.find_elements(By.XPATH, '//button[text()="Manage"]')
        manageButton[1].click()

        time.sleep(2)
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        inputs[0].send_keys(elys)

        time.sleep(5)
        manageButton = driver.find_element(By.XPATH, '//button[text()="Stake ELYS"]')
        manageButton.click()

        time.sleep(15)
        approve(driver)
    except Exception as e:
        print("质押网络异常, 重新执行")
        clean_chrome_extension(driver)
        time.sleep(3)
        stake(driver)


def add_liquidity(driver):
    print("增加流动性任务")
    try:
        driver.get("https://testnet.elys.network/earn/mining")

        time.sleep(15)
        addLiqu = driver.find_elements(By.XPATH, '//span[text()="Add Liquidity"]/..')
        addLiqu[0].click()

        time.sleep(5)

        addLiqu = driver.find_element(By.XPATH, '//span[text()="Single Asset"]/..')
        addLiqu.click()
        
        time.sleep(2)
        
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        inputs[1].send_keys("0.0002")

        time.sleep(5)
        button = driver.find_elements(By.XPATH, '//button[text()="Deposit"]')[1]
        button.click()

        time.sleep(15)
        approve(driver)
    except Exception as e:
        #print(e)
        print("增加流动性网络异常, 重新执行")
        clean_chrome_extension(driver)
        time.sleep(3)
        add_liquidity(driver)


def sign_in(driver):
    driver.get("https://testnet.elys.network")
    time.sleep(random.randint(5, 10))
    try:
        signIn = driver.find_element(By.XPATH, '//a[text()="Sign In"]')
        signIn.click()

        time.sleep(random.randint(2, 10))
        button = driver.find_element(By.XPATH, '//span[text()="Connect with Wallet"]/..')
        button.click()

        time.sleep(random.randint(3, 10))
        button = driver.find_element(By.XPATH, '//span[text()="Keplr"]/../..')
        button.click()

        time.sleep(random.randint(8, 10))
        confirm_chrome_extesion(driver)
    except Exception as e:
        print(e)
        print("钱包登录异常, 准备重试")
        time.sleep(3)
        sign_in(driver)
        return

    time.sleep(15)
    buttons = driver.find_elements(By.XPATH, '//a[text()="Sign In"]')
    if (len(buttons) == 1):
        #重新登录
        sign_in()
        

def refer(driver):
    try:
        driver.get("https://elys.bonusblock.io?r=Bx9DYyYP")
        time.sleep(random.randint(5, 60))

        keplr = driver.find_element(By.XPATH, '//div[text()="Connect with Keplr"]')
        keplr.click()

        time.sleep(random.randint(15, 20))
        confirm_chrome_extesion(driver)

        time.sleep(random.randint(15, 20))
        confirm_chrome_extesion(driver)
    except Exception as e:
        print("网络异常,重新连接")
        refer(driver)


def job_start(private_key, line_number):
    #time.sleep(random.randint(60, 180))
    thread_name = threading.current_thread().name
    print("----------->线程" + thread_name + "开始导入第[" + line_number + "]个钱包")
    
    wallet_name = "keplrWallet" + line_number
    wallet = KelprWallet(private_key, wallet_name, wallet_name)
    driver = wallet.do_import()
    driver._switch_to.window(driver.window_handles[0])
    driver.maximize_window()

    refer(driver)
    time.sleep(random.randint(10, 30))
            
    #登录
    sign_in(driver)
    
    print("钱包" + wallet_name + "登录完成")
    time.sleep(random.randint(10, 20))

    #领水
    claim_deposit(driver)

    time.sleep(random.randint(5, 20))

    #交易
    res = swap(driver)
    if res == -1:
        print(private_key + "无余额==================")
        return

    print("钱包" + wallet_name + "swap完成")
    time.sleep(random.randint(20, 35))

    #质押
    stake(driver)

    print("钱包" + wallet_name + "质押完成")            
    time.sleep(random.randint(25, 35))

    #增加流通性
    add_liquidity(driver)
    time.sleep(random.randint(25, 50))

    print("钱包" + wallet_name + "交互完成")


line_number = 0
with open('wallet.txt', 'r') as f:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for line in f:
            if "#" in line:
                continue
            line_number += 1
            executor.submit(job_start, line, str(line_number))
            time.sleep(random.randint(50, 120))
            
    executor.shutdown(wait=True)
    print("脚本执行完毕")

'''
wallet = KelprWallet('0x4089c7f7ae1b9a6f8111373fd55318658f040fca6d104d41ab82075a6434f74b', 'Keplr12321431', 'Ker000002')
driver = wallet.do_import()

#https://elys.bonusblock.io?r=Bx9DYyYP
driver._switch_to.window(driver.window_handles[0])
driver.maximize_window()
#refer()

#登录
sign_in()

time.sleep(10)

#领水
claim_deposit()

time.sleep(10)

#交易
swap()

time.sleep(30)

#质押
stake()
    
time.sleep(30)

#增加流通性
add_liquidity()

print("脚本执行完毕")
'''
