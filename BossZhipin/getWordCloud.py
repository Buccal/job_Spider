from config import *
import os
import jieba
import wordcloud
from scipy.misc import imread

# 打开文件
os.chdir(r'../Output')

# 打开文件，读取内容
fb = open("jobRequests.txt", "r", encoding="utf-8")
txt = fb.read()
fb.close()

# 对分词进行处理
words = jieba.lcut(txt)
counts = {}
for word in words:
	if len(word) == 1:
		continue
	elif word == "CSS3" or word == "css":
		rword = "CSS"
	elif word == "JavaScript" or word == "javascript" or word == "Javascript" or word == "js" or word == "JS":
		rword = "JavaScript"
	elif word == "vue" or word == "VUE":
		rword = "Vue"
	elif word == "react":
		rword = "React"
	elif word == "html" or word == "HTML5":
		rword = "HTML"
	elif word == "web":
		rword = "Web"
	else:
		rword = word
	counts[rword] = counts.get(rword,0) + 1
for word in excludes:
	print(counts)
	del counts[word]

# 输出前num位
items = list(counts.items())
items.sort(key=lambda x:x[1], reverse=True)
for i in range(num):
	word, count = items[i]
	print ("{0:<10}{1:>5}".format(word, count))

# 生成词云
mask = imread("chinamap.jpg")
picData = " ".join(words)
w = wordcloud.WordCloud(\
    width = 1000, height = 700,\
    background_color = "white",
    font_path = "msyh.ttc", mask = mask
    )
w.generate(picData)
w.to_file("jobRequests.png")