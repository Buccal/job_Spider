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

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# 进行Chrome配置
driverOptions = webdriver.ChromeOptions()
# driverOptions.add_argument('--headless')
driverOptions.add_experimental_option("useAutomationExtension", False) # 关闭插件
driverOptions.add_argument(r'--user-data-dir=C:\Users\Hfour\AppData\Local\Google\Chrome\User Data')
driverOptions.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
# 添加代理
# driverOptions.add_argument("--proxy-server=http://202.20.16.82:10152")

driver = webdriver.Chrome(options=driverOptions, executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')

# driver = webdriver.Chrome()
# driver.set_window_size(1400, 9)
wait = WebDriverWait(driver, 10)

def search(url, search_word):
	print("正在搜索", search_word, "……")
	driver.get(url)
	time.sleep(10)
	try:
		search_input= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#wrap > div.column-search-panel > div > div > div.search-form > form > div.search-form-con > p > input")))
		search_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wrap > div.column-search-panel > div > div > div.search-form > form > button")))
		search_input.clear()
		search_input.send_keys(search_word)
		# search_input.send_keys(Keys.ENTER)
		search_submit.click()
		getJobInfo(1)
	except TimeoutException:
		print("搜索超时。")

def nextPage(pageNum):
	print("正在翻到", str(pageNum), "页……")
	try:
		nextBtn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > div.job-list > div.page > a.next")))
		nextBtn.click()
		wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#main > div > div.job-list > div.page > a.cur"), str(pageNum)))
		getJobInfo(pageNum)
	except TimeoutException:
		print(driver.page_source)
		print("进入下一页超时。")
		#nextPage(pageNum)

def getJobInfo(pageNum):
	print("正在获取第" + str(pageNum) + "页数据……")
	wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > div.job-list > ul > li:last-child > div > div.info-primary div.job-title")))
	html = driver.page_source
	doc = pq(re.sub('xmlns=".*?"', '', html))
	items = doc(".job-list .job-primary").items() #generator类型
	for item in items:
		otherJobInfo = re.findall(r'(.*?)<em class="vline"/>(.*)', str(item.find(".job-limit > p").html()), re.S)
		otherCompanyInfo = re.findall(r'<em class="vline"/>(.*?)<em class="vline"/>(.*)', str(item.find(".company-text > p").html()), re.S)
		jobInfo = {
			'jobTitle': item.find(".job-name a").text(),
			'detailLink': url + item.find(".primary-box").attr("href"),
			'salary': item.find(".job-limit > .red").text(),
			'location': item.find(".job-area").text(),
			'experience': '',
			'education': '',
			'companyName': item.find(".info-company h3.name > a").text(),
			'industry': item.find(".company-text > p > a").text(),
			'goPublic': '',
			'employeesNum': ''
		}
		if len(otherJobInfo):
			jobInfo['experience'], jobInfo['education'] = otherJobInfo[0]
		if len(otherCompanyInfo):
			jobInfo['goPublic'], jobInfo['employeesNum'] = otherCompanyInfo[0]
		# print(json.dumps(jobInfo, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
		saveToMongo(jobInfo)
	print("第" + str(pageNum) + "页数据存储完成。")

def saveToMongo(result):
	try:
		if db[MONGO_TABLE].insert_one(result):
			print('成功插入一条数据。')
			# print('成功插入一条数据', result)
	except Exception:
		print("存储到数据库发生异常。")

def main():
	try:
		search(url, keyWord)
		for num in range(2, 11):
			nextPage(num)
	except Exception:
		print("出现异常。")
	finally:
		driver.quit()

if __name__ == '__main__':
	main()
