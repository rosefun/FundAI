#!/usr/env/bin python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
import re
import ast
import pandas as pd
import numpy as np

# 抓取网页
def get_url(url, params=None):
    """
    爬取天天基金中基金的最新估值。
    e.g. http://fundgz.1234567.com.cn/js/161725.js?rt=1589463125600
    return: html
    """
    rsp = requests.get(url, params=params)
    rsp.raise_for_status()
    return rsp.text

def get_fund_data(fundcode, base_url="http://fundgz.1234567.com.cn/js/"):
    """
    name: 基金名称
    jzrq:截止日期
    dwjz:单位净值
    gsz:估算值
    gszzl:估算增长率
    gztime:估值时间
    请求数据，处理html数据
    return: dict type.
    """
    url = base_url + str(fundcode) + ".js"
    html = get_url(url)
    context = html.replace("jsonpgz","").replace(";","").replace("(","").\
    replace(")","")
    if len(context) == 0:
        return None
    context = ast.literal_eval(context)
    # 
    name = context["name"]
    jzrq = context["jzrq"]
    dwjz = context["dwjz"]
    gsz = context["gsz"]
    gszzl = context["gszzl"]
    gztime = context["gztime"]
    
    print("基金名称:{}, 截止日期:{}, 单位净值:{}, 估算值:{}, 估算增长率:{}, 估值时间:{}".format(
    name, jzrq, dwjz, gsz, gszzl, gztime))
    return context

def get_fundcode(path):
    """
    csv file.
    return fundcode.
    改用：http://fund.eastmoney.com/js/fundcode_search.js
    """
    fund_df = pd.read_csv(path, sep=",", engine="python", dtype={"基金代码": "object"})
    fundcode = fund_df["基金代码"].tolist()

    return fundcode
    
def get_all_fundcode(base_path=r"F:\研究生\github项目\基金AI\FundCrawler\results"):
    """
    获取基金代码。
    
    """
    fundtypeList = ["QDII-指数", "股票型", "股票指数", "混合型", "联接基金", "债券型"]
    all_fundcode = []
    # QDII-指数
    for fundtype in fundtypeList:
        path = base_path + "\{}.csv".format(fundtype)
        fundcode = get_fundcode(path)
        all_fundcode += fundcode
    
    return all_fundcode

from pandas.tseries.offsets import BusinessDay
def get_last_business_day(offset, today=None):
    """
    返回offset个工作日的日期。
    e.g. offset:7, today:2021.03.18; return: 2021-03-09
    return: string type.
    """
    if today is None:
        today = pd.datetime.today()
    last_offset_day = today - BusinessDay(offset)
    
    string = last_offset_day.to_pydatetime()
    str_day = str(string).split()[0]
    #print(type(str_day), str_day)
    return str_day

def get_latest_funddata(fundcode, per=10,sdate='',edate=''):
    """
    获取最近7天的基金数据
    code:基金代码
    page:页码
    per:每页数量
    sdate:开始日期
    edate:截止日期
    """
    today = pd.datetime.today()
    today = str(today).split()[0]#.strftime("%Y-%M-%D")

    last_week_Bday = get_last_business_day(offset=7)
    #print("last_week_Bday", last_week_Bday)
    # 获取近一周的基金数据
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {'type': 'lsjz', 'code': fundcode, 'page':1,'per': per, 'sdate': last_week_Bday, 'edate': today}
    html = get_url(url, params)
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)
    
    # # 获取总页数
    # pattern=re.compile(r'pages:(.*),')
    # result=re.search(pattern,html).group(1)
    # pages=int(result)
    # print("pages", pages)
    # 获取表头
    heads = []
    for head in soup.findAll("th"):
        heads.append(head.contents[0])
    print("heads", heads)
    
    # 获取数据
    records = []
    for row in soup.findAll("tbody")[0].findAll("tr"):
        row_records = []
        for record in row.findAll('td'):
            val = record.contents

            # 处理空值
            if val == []:
                row_records.append(None)
            else:
                row_records.append(val[0])

        # 记录数据
        records.append(row_records)
    print("records", records)
    # 数据整理到dataframe
    np_records = np.array(records)
    print("np_records", np_records)
    if len(np_records[0]) <= 1:
        return None
    min_jz = min(np_records[:,1].astype(np.float))
    #print(min_jz)
    return min_jz


def main():
    # fund code
    all_fundcode = get_all_fundcode()
    tobuyfund = []
    # 请求数据
    for fundcode in all_fundcode:
        res_dict = get_fund_data(fundcode=fundcode)
        if res_dict is None:
            continue
        # 现在估值
        gsjz = res_dict['gsz']
        if gsjz is None:
            continue
        # 近7天最低单位净值
        min_ljjz = get_latest_funddata(fundcode=fundcode)
        if min_ljjz is None:
            continue
        zf = (float(gsjz) - float(min_ljjz))/float(min_ljjz)
        print("估算净值:{}, 7天最近单位净值:{}, 增幅:{}".format(gsjz, min_ljjz, zf))
        if zf < -0.08:
            print("值得低价买入", fundcode)
            tobuyfund.append([fundcode, zf])
    print(tobuyfund)

if __name__ == "__main__":
    #main()
    print(get_last_business_day(7))
    get_latest_funddata(fundcode=161725)
    main()
