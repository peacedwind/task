from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

'''
class KelprWallet():
    def __init__(self, private_key, wallet_name, wallet_pwd):
        self.private_key = private_key
        self.wallet_name = wallet_name
        self.wallet_pwd = wallet_pwd

    def do_import(self):
        print("开始导入钱包:" + self.wallet_name)
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_extension('crx/keplr.crx')
        driver = webdriver.Chrome(options=chrome_options)

        time.sleep(5)

        for wh in driver.window_handles:
            driver._switch_to.window(wh)
            if 'chrome-extension' in driver.current_url:
                print("切换到窗口: " + driver.current_url)
                driver._switch_to.window(wh) #切换到keplr钱包窗口
                break

        # 加载插件, 导入钱包
        time.sleep(3)
        importWalletButton = driver.find_elements(By.TAG_NAME, 'button') # import wallet
        importWalletButton[1].click()

        time.sleep(3)
        importWalletButton2 = driver.find_elements(By.TAG_NAME, 'button') # import wallet
        importWalletButton2[3].click()

        time.sleep(1)
        privateKey = driver.find_element(By.XPATH, '//button[text()="Private key"]') # 选择导入方式为私钥
        privateKey.click()

        time.sleep(1)
        privateKeyInput = driver.find_element(By.TAG_NAME, 'input')
        privateKeyInput.send_keys(self.private_key) #私钥
        
        time.sleep(1)
        privateKeyInputConfirm = driver.find_element(By.XPATH, '//button[@type="submit"]')
        privateKeyInputConfirm.click()

        #钱包设置
        time.sleep(1)
        walletInputs = driver.find_elements(By.TAG_NAME, 'input')
        walletInputs[1].send_keys(self.wallet_name)
        walletInputs[2].send_keys(self.wallet_pwd)
        walletInputs[3].send_keys(self.wallet_pwd)
        walletInputConfirms = driver.find_elements(By.XPATH, '//button[@type="submit"]')
        walletInputConfirms[1].click()

        time.sleep(5)
        save = driver.find_element(By.TAG_NAME, 'button')
        save.click()

        time.sleep(2)
        finish = driver.find_element(By.TAG_NAME, 'button')
        finish.click()

        print("钱包导入完成")

        return driver    
'''

class OkxWallet():
    def __init__(self, private_key, wallet_name, wallet_pwd):
        self.private_key = private_key
        self.wallet_name = wallet_name
        self.wallet_pwd = wallet_pwd

    def do_import(self):
        print("开始导入钱包:" + self.wallet_name)
            
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_extension('crx/okx.crx')
        driver = webdriver.Chrome(options=chrome_options)

        time.sleep(5)
        driver._switch_to.window(driver.window_handles[0])
        driver.close()
        
        for wh in driver.window_handles:
            driver._switch_to.window(wh)
            if 'chrome-extension' in driver.current_url:
                print("切换到窗口: " + driver.current_url)
                break

        time.sleep(3)
        importWalletButton = driver.find_elements(By.TAG_NAME, 'button')[1]
        importWalletButton.click()

        time.sleep(1)
        private_key_button = driver.find_element(By.XPATH, '//div[text()="助记词或私钥"]')
        private_key_button.click()

        time.sleep(1)
        private_key_button = driver.find_element(By.XPATH, '//div[text()="私钥"]')
        private_key_button.click()

        time.sleep(1)
        wallet_input = driver.find_element(By.TAG_NAME, 'textarea')
        wallet_input.send_keys(self.private_key)

        time.sleep(2)
        walletInputConfirms = driver.find_elements(By.XPATH, '//button[@type="submit"]')
        walletInputConfirms[1].click()

        time.sleep(2)
        wallet_input_confirm = driver.find_element(By.XPATH, '//button[@type="button"]')
        wallet_input_confirm.click()

        time.sleep(3)
        pw_inputs = driver.find_elements(By.TAG_NAME, 'input')
        pw_inputs[0].send_keys(self.wallet_pwd)
        pw_inputs[1].send_keys(self.wallet_pwd)

        time.sleep(5)
        pw_confirm = driver.find_element(By.XPATH, '//button[@type="submit"]')
        pw_confirm.click()

        time.sleep(8)
        confirms = driver.find_elements(By.XPATH, '//button[@type="button"]')
        confirms[0].click()

        time.sleep(2)
        driver.close()

        print("钱包[" + self.wallet_name + "]导入完成")
        return driver
