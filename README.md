# 智能选择优质基金

### 1. 关于本项目

​	本项目希望能够通过每天爬取基金数据，通过一些金融知识或者机器学习模型，给出当天优质基金。

### 2. 基金数据爬取

​	python3运行code中`CrawlingFund.py` 代码。

​	爬取网站：好买基金 https://www.howbuy.com/fund/fundranking

​	获取数据有，股票型，债券型，混合型，理财型，货币性，指数型，结构型，对冲型，QDII型基金，数据格式CSV文件。



### 3. 筛选优质基金

#### 3.1 金融知识

​	**4433法则**：一只好的基金要同时满足以下条件：

​	1.近1年业绩排名在同类基金中位列前1/4；

​	2.近2/3/5年业绩排名在同类基金中位列前1/4；

​	3.近3个月业绩排名在同类基金中位列前1/3；

​	4.近6个月业绩排名在同类基金中位列前1/3。

#### 3.2 机器学习模型

​	根据每周或者每月或者每半年等时间维度基金涨幅为预测目标，构建回归模型，预测各个基金的涨幅。
