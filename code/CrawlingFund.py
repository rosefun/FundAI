# encoding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time

def extract_url_info(url="https://www.howbuy.com/fund/fundranking/", scroll_times=0):
    
    driver = webdriver.Chrome(executable_path="E:\软件安装\Google Chrome\chromedriver_win32_87\chromedriver.exe")#用chrome浏览器打开
    driver.get(url)       
    time.sleep(2)                            #让操作稍微停一下
    cookie = driver.get_cookies()
    time.sleep(2)
    
    # 滚动鼠标
    def execute_times(times):
        for i in range(times):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
    execute_times(scroll_times)
    
    info_list = []
    
    html = driver.page_source
    soup1 = BeautifulSoup(html,'lxml')    
    count = 0
    for info in soup1.find_all('tr'):
        try:
            #print(len(info.find_all('td')))
            # 基金链接及名称
            td = info.find_all('td')[3]
            link = td.find('a').get('href')
            name = td.find('a').contents[0]

            # 基金代码
            td = info.find_all('td')[0]
            code = td.find('input').get("value")
            # 日期 净值 近一周 近一月 近三月 近半年 近一年 今年以来
            td = info.find_all('td')[4]
            date = td.contents[0]
            jingzhi = info.find_all('td')[5].contents[0]
            week_change = info.find_all('td')[6].find('span').contents[0]
            month_change = info.find_all('td')[7].find('span').contents[0]
            threemonth_change = info.find_all('td')[8].find('span').contents[0]
            halfyear_change = info.find_all('td')[9].find('span').contents[0]
            year_change = info.find_all('td')[10].find('span').contents[0]
            thisyear_change = info.find_all('td')[11].find('span').contents[0]
            # 基金的信息
            assert str(code) in str(link)
            header = "基金代码,基金名称,日期,净值,近一周,近一月,近三月,近半年,近一年,今年以来,基金的详细链接"
            result = "{},{},{},{},{},{},{},{},{},{},{}".format(code, name, date, jingzhi, week_change, month_change, threemonth_change, 
            halfyear_change, year_change, thisyear_change, link)
            #print(result)
            info_list.append(result)
            count += 1
        except Exception as e:
            print("error", e)
    print("基金数量", count)
    #driver.close()
    return info_list, header
    
def main():
    # 股票型,...
    url_list = ["https://www.howbuy.com/fund/fundranking/gupiao.htm", "https://www.howbuy.com/fund/fundranking/zhaiquan.htm",
    "https://www.howbuy.com/fund/fundranking/hunhe.htm", "https://www.howbuy.com/fund/fundranking/licai.htm", 
    "https://www.howbuy.com/fund/fundranking/huobi.htm", "https://www.howbuy.com/fund/fundranking/zhishu.htm",
    "https://www.howbuy.com/fund/fundranking/jiegou.htm", "https://www.howbuy.com/fund/fundranking/qdii.htm",
    "https://www.howbuy.com/fund/fundranking/duichong.htm"]
    if not os.path.exists('./result/'):
        os.makedirs('./result/')
            
    for url in url_list:
        type = url.split("/")[-1].replace(".htm", "")
        print("type", type)
        info_list,header = extract_url_info(url=url, scroll_times=13)
        with open("./result/haomai_{}.csv".format(type), "w", encoding="utf-8") as f:
            f.write(header)
            f.write('\n')
            for info in info_list:
                f.write(str(info))
                f.write('\n')
    exit(0)


if __name__ == "__main__":
    main()