from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wallet import KelprWallet
import time


def clean_chrome_extension():
    curWindows = driver.current_window_handle
    for wh in driver.window_handles:
        driver._switch_to.window(wh)
        if "chrome-extension" in driver.current_url:
            driver.close()
            break
    
    driver._switch_to.window(curWindows)
    

def confirm_chrome_extesion():
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


def approve():
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


def claim_deposit():
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

        time.sleep(30) #等待领取完成
    except Exception as e:
        print("领取失败, 准备重试")
        time.sleep(1)
        claim_deposit()

    #claim = driver.find_elements(By.XPATH, '//button[text()="Claim Tokens"]')
    #if (len(claim)) == 1:
        #driver.refresh()
        #claim_deposit()


def swap():
    try:
        js='window.open("https://testnet.elys.network/swap#USDC/ELYS");'

        driver.execute_script(js)

        usdc = '0.01'
        print("swap任务, 交易USDC: " + usdc)

        time.sleep(5)
        driver.switch_to.window(driver.window_handles[1])

        time.sleep(8)
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        time.sleep(1)
        inputs[0].send_keys(usdc)

        time.sleep(3)
        receive = driver.find_element(By.XPATH, '//button[text()="Receive ELYS"]')
        receive.click()

        time.sleep(15)
        approve()
    except Exception as e:
        print("交易时网络异常, 重新执行")
        clean_chrome_extension()
        driver.close()
        time.sleep(3)
        swap()

def stake():
    try:   
        driver.get("https://testnet.elys.network/earn/staking")

        time.sleep(5)

        elys = '0.01'
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
        approve()
    except Exception as e:
        print("质押网络异常, 重新执行")
        clean_chrome_extension()
        time.sleep(3)
        stake()


def add_liquidity():
    print("增加流动性任务")
    try:
        driver.get("https://testnet.elys.network/earn/mining")

        time.sleep(15)
        addLiqu = driver.find_elements(By.XPATH, '//span[text()="Add Liquidity"]/..')
        addLiqu[0].click()

        time.sleep(5)
        inputs = driver.find_elements(By.TAG_NAME, 'input')
        inputs[1].send_keys("0.005")

        time.sleep(5)
        button = driver.find_elements(By.XPATH, '//button[text()="Deposit"]')[1]
        button.click()

        time.sleep(15)
        approve()
    except Exception as e:
        #print(e)
        print("增加流动性网络异常, 重新执行")
        clean_chrome_extension()
        time.sleep(3)
        add_liquidity()


def sign_in():
    driver.get("https://testnet.elys.network")
    time.sleep(5)
    try:
        signIn = driver.find_element(By.XPATH, '//a[text()="Sign In"]')
        signIn.click()

        time.sleep(2)
        button = driver.find_element(By.XPATH, '//span[text()="Connect with Wallet"]/..')
        button.click()

        time.sleep(3)
        button = driver.find_element(By.XPATH, '//span[text()="Keplr"]/../..')
        button.click()

        time.sleep(8)
        confirm_chrome_extesion()
    except Exception as e:
        print("钱包登录异常, 准备重试")
        time.sleep(3)
        sign_in()

    time.sleep(15)
    buttons = driver.find_elements(By.XPATH, '//a[text()="Sign In"]')
    if (len(buttons) == 1):
        #重新登录
        sign_in()
        

def refer():
    try:
        driver.get("https://elys.bonusblock.io?r=Bx9DYyYP")
        time.sleep(5)

        keplr = driver.find_element(By.XPATH, '//div[text()="Connect with Keplr"]')
        keplr.click()

        time.sleep(15)
        confirm_chrome_extesion()

        time.sleep(15)
        confirm_chrome_extesion()
    except Exception as e:
        print("网络异常,重新连接")
        refer()


wallet = KelprWallet('--', 'Keplr', 'ccsu00001')
driver = wallet.do_import()

#https://elys.bonusblock.io?r=Bx9DYyYP
driver._switch_to.window(driver.window_handles[0])
refer()

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

