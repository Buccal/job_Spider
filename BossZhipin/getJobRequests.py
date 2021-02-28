from config import *
import pymongo
import os

# 读取数据库
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_TABLE]

# 打开文件
os.chdir(r'../Output')

# 写入数据库中查询结果
fb = open('jobRequests.txt', 'w+', encoding='utf-8')
results = collection.find()
for result in results:
	if 'jobDetail' in result:
		if("实习" in result['jobTitle'] or "校招" in result['jobTitle'] or "应届" in result['jobTitle'] or result['jobDetail'] is None):
			print("跳过")
		else:
			# fb.writelines([result['jobTitle'], "\n", result['salary'],  "\n", result['jobDetail'], '\n\n'])
			fb.writelines([result['jobDetail'], '\n\n'])
			print("插入一条")
fb.close()
