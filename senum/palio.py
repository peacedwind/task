import time

import common
import account
# 首先获取全部的账号
account_list = account.get_all_accounts()




if len(account_list) > 0:
    for account in account_list:
        private_key = account.private_key
        password = account.wallet_password
        # 导入钱包
        driver = common.import_wallet(private_key,password)
        common.switch_first_win()
        driver.get('https://xter.io/activities/palio')
        ## 链接钱包
        time.sleep(100)

