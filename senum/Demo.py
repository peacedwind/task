import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
elem = driver.find_element(by=By.NAME,value="q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
time.sleep(5)
driver.find_element(by=By.XPATH,value="//a[@href='/blogs/']").click()
time.sleep(5)

## 给搜索框赋值
kw = driver.find_element(by=By.ID,value="kw")
kw.send_keys("python官网")
# 点击百度一下
su = driver.find_element(by=By.ID,value="su")
## 提交
su.click()
## 获取第一个链接
time.sleep(5)
res_list = driver.find_element(by=By.ID,value="content_left")
first = res_list.find_element(by=By.TAG_NAME,value="div")
first = first.find_element(by=By.TAG_NAME,value="a")
first.click()

## 跳转以后获取元素
time.sleep(10)

driver._switch_to.window(driver.window_handles[1])
## 获取输入框
elem = driver.find_element(by=By.NAME,value="q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
time.sleep(10)