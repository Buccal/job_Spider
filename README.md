# job_Spider Readme

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

本库目前实现以下内容：

1. 使用selenium对Boss直聘进行爬虫，将工作信息（岗位头衔、薪资、地点、经验要求、学历要求、公司名称、所属行业、融资情况、人员规模、岗位详情）使用MongoDB存储到本地数据库中
2. 筛选符合要求的工作，保存对应的岗位要求
3. 对所有岗位要求分词，并生成词云


## 目录

- [背景](#背景)
- [安装](#安装)
- [使用](#使用)
- [例子](#例子)
- [参考](#参考)
- [License](#license)

## 背景

2019年底在GitHub没找到未过期的Boss直聘爬虫，写了这个。

2021年初运行代码已过期，修改了部分代码，截止2021-03-01可用。

## 安装

1. 安装[python](https://www.python.org/downloads/)或Anaconda3[镜像](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)（推荐阅读：[Anaconda下载换源](https://www.jianshu.com/p/02b053b8143a)）
2. 安装[MongoDB](https://www.mongodb.com/try/download/community)
3. 安装[Robo3T](https://studio3t.com/download/?source=robomongo&medium=homepage)
4. 安装python库requests、pymongo、selenium、pyquery、imageio、pymongo、jieba、wordcloud
5. 安装Chrome
6. 安装与Chrome版本号一致的ChromeDriver[镜像](https://npm.taobao.org/mirrors/chromedriver/)，放到chrome.exe文件目录下

eg.

**python：**
```
pip install requests
```

**Anaconda3：**
```
conda install requests
conda install -c conda-forge jieba
conda install -c conda-forge wordcloud
```

## 使用

### 文件的顺序和作用
**可执行文件**
1. `BossZhipin/main.py`：爬取工作基本信息存储到数据库
2. `BossZhipin/getJobDetails.py`：爬取工作详情页信息存储到数据库
3. `BossZhipin/getJobRequests.py`：筛选符合要求的工作，汇总岗位信息保存到`Output/jobRequests.txt`
4. `BossZhipin/getWordCloud.py`：读取岗位信息，生成词云，并根据词频输出关键词

**其他文件**
- `BossZhipin/config.py`：配置文件
- `Output/chinamap.jpg`：词云的形状
- `Output/jobRequests.txt`：汇总的岗位信息，可根据需要修改内容
- `Output/jobRequests.png`：生成的词云

### 配置config.py
1. `MONGO_URL、MONGO_DB、MONGO_TABLE`：本地数据库配置
2. `url`：Boss直聘首页链接
3. `keyWord`：搜索岗位关键词
4. `excludes`：统计词频时的排除单词
5. `num`：输出词频排名前几位

### Chrome
1. 注册Boss直聘，在Chrome上登录并记住账号
2. 当运行`main.py`在首页不断刷新，关闭爬虫，重新打开Chrome，进入Boss直聘首页，通过安全验证，再关闭Chrome执行代码


## 例子

![Pic of Database](https://raw.githubusercontent.com/Buccal/job_Spider/main/Screenshots/2021-03-01_204213.png)

![Pic of WordCloud](https://raw.githubusercontent.com/Buccal/job_Spider/main/Output/jobRequests.png)

![Pic of WordCloud](https://raw.githubusercontent.com/Buccal/job_Spider/main/Output/2021-03-01_205417.png)


## 参考




## License

[MIT](LICENSE) © Buccal
