#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from wallet import OkxWallet
import concurrent.futures
import time
#import sys
import random
import threading

def clean_chrome_extension(driver):
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

    approve = driver.find_element(By.XPATH, '//div[text()="连接"]')
    approve.click()

    driver._switch_to.window(curWindows)


def approve(driver):
    curWindows = driver.current_window_handle
    flag = False
    for wh in driver.window_handles:
        driver._switch_to.window(wh)
        if "chrome-extension" in driver.current_url:
            print("钱包插件确认...")
            driver._switch_to.window(wh)
            flag = True
            break

    if flag:
        approve = driver.find_elements(By.TAG_NAME, 'button')[1]
        approve.click()
    
    driver._switch_to.window(curWindows)


def page_load(driver):
    print("加载页面...")
    try:
        driver.get("https://pioneer.particle.network?inviteCode=D2YHP0")#

        time.sleep(8)
        open_wallet = driver.find_element(By.XPATH, '//span[text()="JOIN"]')
        open_wallet.click()

        time.sleep(3)
        open_wallet = driver.find_element(By.XPATH, '//span[text()="okx Wallet"]')
        open_wallet.click()

        time.sleep(5)
        confirm_chrome_extesion(driver)

        time.sleep(5)
        approve(driver)
    except Exception as e:
        print("重新加载页面...")
        time.sleep(3)
        page_load(driver)

def switch_frame(driver):
    thread_name = threading.current_thread().name
    try:
        driver.get("https://pioneer.particle.network/zh-CN/point")
        time.sleep(5)

        #particle-pwe-wallet-icon
        #open_wallet = driver.find_element(By.XPATH, '//span[text()="Open Wallet"]')
        open_wallet = driver.find_element(By.CSS_SELECTOR, ".particle-pwe-wallet-icon")
        open_wallet.click()

        time.sleep(15)
        iframe = driver.find_element(By.CSS_SELECTOR, ".particle-pwe-iframe")
        driver.switch_to.frame(iframe)
        print(thread_name + ", 切换到iframe")

        change_network(driver)
    except Exception as e:
        print("窗口切换异常, ", e)
        time.sleep(3)
        window_handles = driver.window_handles
        if len(window_handles) > 1:
            print(len(window_handles))
            clean_chrome_extension(driver)
        switch_frame(driver)


def do_send(driver, send_times, retry_delay):
    #network = driver.find_element(By.XPATH, '//span[text()="Ethereum Sepolia"]')
    time.sleep(random.randint(5, 10))
    send = driver.find_element(By.XPATH, '//div[text()="Send"]')
    send.click()

    time.sleep(5)
    send = driver.find_element(By.ID, 'send_to')
    send.send_keys("0x29b4cbcf10d6f8d784c996f3d165121c846efa77")#发送到对应的地址

    time.sleep(1)
    send = driver.find_element(By.ID, 'send_amount')
    send_value = random.uniform(0.0001, 0.0009)
    send.send_keys(str(round(send_value, 4)))

    time.sleep(5)
    send = driver.find_element(By.XPATH, '//button[@type="submit"]')
    send.click()

    time.sleep(random.randint(25, 45))
    send = driver.find_elements(By.XPATH, '//span[text()="Send"]/..')
    send[len(send) - 1].click()

    if retry_delay > 0:
        print("重试延时时间: " + str(retry_delay))
    
    time.sleep(random.randint(15, 20) + retry_delay)
    if send_times == 1:
        time.sleep(random.randint(120, 150) + retry_delay)
   
    approve(driver)

    time.sleep(random.randint(15, 25))

def job_start(start, end, delay):
    thread_name = threading.current_thread().name

    print("线程" + thread_name + "开始交易第" + str(start) + "到" + str(end) + "次")
    time.sleep(delay)
    
    private_key = ""
    wallet_name = "OkxWallet" + str(delay)
    wallet = OkxWallet(private_key, wallet_name, wallet_name)
    driver = wallet.do_import()
    driver._switch_to.window(driver.window_handles[0])
    driver.maximize_window()

    print(driver)
    page_load(driver)

    retry_times = 0
    send_times = 1
    i = end - start
    while send_times <= i:
        print(thread_name + "发送进度: " + str(send_times) + "/" + str(i))
        time.sleep(5)
        switch_frame(driver)
        time.sleep(3)

        try:
            retry_delay = retry_times * 10
            do_send(driver, send_times, retry_delay)

            send_times += 1
        except Exception as e:
            print(thread_name + " 发送异常, ", e)
            clean_chrome_extension(driver)
            retry_times += 1

        driver.refresh()

    print("线程" + thread_name + "执行完毕, 次数:" + str(i))


def change_network(driver):
    network = driver.find_elements(By.XPATH, '//span[text()="BNB Chain Testnet"]')
    print("change_network: " + str(len(network)))
    if len(network) == 0:
        network = driver.find_element(By.CSS_SELECTOR, ".m-network")
        network.click()
        time.sleep(2)

        network = driver.find_element(By.XPATH, '//span[text()="BNB Chain Testnet"]')
        network.click()
        time.sleep(random.randint(10, 20))
        approve(driver)

        time.sleep(1)
        iframe = driver.find_element(By.CSS_SELECTOR, ".particle-pwe-iframe")
        driver.switch_to.frame(iframe)
        
    
total_iterations = 10
thread_num = 3
iterations_per_thread = total_iterations // thread_num
remaining_iterations = total_iterations % thread_num

with concurrent.futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
    start = 0
    for i in range(thread_num):
        end = start + iterations_per_thread
        if i < remaining_iterations:
            end += 1  # 将多余的任务分配给前面的线程

        delay = (28 + i) * i
        executor.submit(job_start, start, end, delay)
        start = end
        time.sleep(1)

executor.shutdown(wait=True)
print("脚本执行完毕")
