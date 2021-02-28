from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import json
import re
from config import *
import pymongo
import time

# 读取数据库
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_TABLE]

# 进行Chrome配置
driverOptions = webdriver.ChromeOptions()
driverOptions.add_experimental_option("useAutomationExtension", False) # 关闭插件
driverOptions.add_argument(r'--user-data-dir=C:\Users\Hfour\AppData\Local\Google\Chrome\User Data')
driverOptions.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(options=driverOptions, executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
wait = WebDriverWait(driver, 10)

def getJobRequests(url):
	print("正在搜索", url, "……")
	driver.get(url)
	try:
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail-content > .job-sec > .text")))
		html = driver.page_source
		doc = pq(re.sub('xmlns=".*?"', '', html))
		print(doc)
		data = doc('.detail-content > .job-sec > .text').text()
		return data
	except TimeoutException:
		print(driver.page_source)
		print("访问超时。")

def main():
	results = collection.find()
	for result in results:
		print(result)
		# print(hasattr(result, "jobDetail"))
		if hasattr(result, "jobDetail") and result["jobDetail"]:
			print("已存在，跳过")
		else:
			# print(getJobRequests(result['detailLink']))
			collection.update_one({'_id':result['_id']},{'$set' : {'jobDetail': getJobRequests(result['detailLink'])}})
			print("成功插入信息")
		# break

if __name__ == '__main__':
	main()



