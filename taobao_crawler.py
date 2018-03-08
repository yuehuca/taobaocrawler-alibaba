# -*- coding: utf-8 -*-

import re
import requests
import os
import time
from bs4 import BeautifulSoup
import random
import pandas as pd
import winsound

os.chdir("F:/python_workshop/pachong") #修改当前工作目录
os.getcwd() #获取当前工作目录

target_list = ["神舟笔记本","联想笔记本"] #写入想爬取的关键词

url_target = 'https://s.taobao.com/search' #需要采集的网址（淘宝）
payload = {'q': '目标','s': '1','ie':'utf8','sort': 'sale-desc'}  #通过字典传递url参数，q为商品名称
merge_path = 'F:/python_workshop/pachong/目标' #设置保存路径和文件名
csvname = '.csv' #添加csv后缀
numberofpages = 101 #需要采集的页数
maxiploops = 20 #允许的某一ip的最大循环次数
maxdelay = 6 #设置最大延迟时间
ipdelay = 0.1 #设置更换ip失败后的等待时间
timeout = 5 #设置request.get()的超时时限

def get_ip_list(url, headers): #获取代理ip函数，返回ip列表
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    print('....代理ip列表采集完成')
    return ip_list

def get_random_ip(ip_list): #随机选择一个代理ip
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/' #免费代理ip获取网站
    referer_list = ["https://www.baidu.com/","https://www.sogou.com/","https://www.so.com/","http://www.bing.com","http://www.chinaso.com/"]
    #设置参考链接表
    ua_list = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) App leWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53",
    "Mozilla/5.0 (Windows NT 8.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.72 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]
    #设置伪装UA列表
    global headers
    headers = {
        'Referer':'http://www.baidu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 8.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
        'Accept-Language':'zh-CN'
    } #referer伪装请求转自哪里，user-agent伪装成浏览器
    #ip_list = get_ip_list(url, headers=headers) #获取代理ip
    #proxies = get_random_ip(ip_list) #定义proxies为从ip_list中随机选取的一个ip地址

def proxytest(): #随机一个ip地址并测试该地址是否可用，返回一个可用ip
    print('....开始更换代理ip')
    proxytestsignal = 0 #测试信号，初始值为0
    print('....随机一个ip、Referer和UA')
    proxies = get_random_ip(ip_list) #随机一个ip
    headers['Referer'] = random.choice(referer_list) #随机一个Referer
    headers['User-Agent'] = random.choice(ua_list) #随机一个UA
    while proxytestsignal == 0: #若信号为0，则表示无法接通
        try:
            print('....测试请求发送中')
            #requests.get('http://wenshu.court.gov.cn/', proxies=proxies) #测试ip
            requests.get('http://www.anzhi.com/', proxies=proxies, headers=headers, timeout=timeout) #测试ip
            print('....测试请求发送成功')
        except:
            print('....代理ip连接失败，等待'+str(ipdelay)+'秒后尝试下一个')
            headers['Referer'] = random.choice(referer_list) #随机一个Referer
            headers['User-Agent'] = random.choice(ua_list) #随机一个UA
            proxies = get_random_ip(ip_list) #若不可用，则再随机一次
            proxytestsignal = 0
            #time.sleep(random.randrange(0,ipdelay*100,1)/100) #在给定时间范围内随机延迟
        else:
            proxytestsignal = 1 #若ip可用，则跳出循环
            print('....代理ip连接成功')
    return proxies

def getdata(url_target,payload,numberofpages,maxiploops,merge_path): #采集过程
    x_0 = 1 #初始化采集结果的索引
    global merge_accumulation
    merge_accumulation = [] #清空采集结果
    for k in range(0,numberofpages): #循环采集过程
        print('..开始采集第'+str(k+1)+'页')
        def changeip(): #changeip()函数，若当前ip的循环次数超过最大允许次数，则更换ip
            global currentiploop #将currentiploop变量全局化
            if k == 0: #若为首轮采集，则初始化currentiploop为0
               currentiploop = 0
            currentiploop = currentiploop + 1 #记录该ip的一轮采集
            print('....该ip已完成'+str(currentiploop)+'轮采集')
            randomiploops = random.randrange(1,maxiploops+1,1) #随机选取一个ip循环最大次数
            if currentiploop >= randomiploops: #若该ip本轮采集的次数大于等于最大允许采集次数，则更新ip
               currentiploop = 0 #归零ip循环计数器currentiploop
               print('....该ip已达到循环阀值，更换ip')
               proxytest() #随机一个ip地址并执行ip测试过程
        headers['Referer'] = random.choice(referer_list) #随机一个Referer
        headers['User-Agent'] = random.choice(ua_list) #随机一个UA
        payload ['s'] = 44*k+1 #此处改变的url参数为s，s为1时第一页，s为45是第二页，89时第三页以此类推   
        getsignal = 0 #页面下载信号，初始值为0                       
        while getsignal == 0: #当采集失败时，重复本轮采集，直到成功为止
            try:
               print('....采集请求发送中')
               resp = requests.get(url_target, params = payload, headers=headers, proxies=proxies,timeout=timeout) #采集淘宝搜索页面
               #resp = requests.get(url_target, params = payload, headers=headers,timeout=timeout) #采集淘宝搜索页面，此为不使用代理
               print('....采集请求发送成功')
            except:
               print('....采集失败，重试')
               #winsound.Beep(600, 1000) #若本次采集失败，则发出报警音
               getsignal = 0
            else:
               getsignal = 1 #若采集成功，则跳出本轮采集，爬虫继续执行
               print('..第'+str(k+1)+'页下载成功')
        resp.encoding = 'utf-8' #设置编码
        print('..正在解析第'+str(k+1)+'页')
        resp_text = resp.text #解析页面
        #将空值替换为none或0
        resp_text_raw_title = resp_text.replace('"raw_title":""','"raw_title":"none"') #清理商品名称
        resp_text_nid = resp_text.replace('"nid":""','"nid":"none"') #清理商品id
        resp_text_category = resp_text.replace('"category":""','"category":"none"') #清理商品类别
        resp_text_view_price = resp_text.replace('"view_price":""','"view_price":"none"') #清理价格
        resp_text_view_sales = resp_text.replace('"view_sales":""','"view_sales":"none"') #清理销售量
        resp_text_comment_count = resp_text.replace('"comment_count":""','"comment_count":"none"') #清理评论
        resp_text_nick = resp_text.replace('"nick":""','"nick":"none"') #清理商铺名称
        resp_text_user_id = resp_text.replace('"user_id":""','"user_id":"none"') #清理商家id
        resp_text_item_loc = resp_text.replace('"item_loc":""','"item_loc":"none"') #清理商铺地址
        resp_text_isTmall = resp_text.replace('"isTmall":""','"isTmall":"none"') #清理天猫属性
        resp_text_sellerCredit = resp_text.replace('"sellerCredit":,','"sellerCredit":0,') #清理卖家信用
        resp_text_totalRate = resp_text.replace('"totalRate":}','"totalRate":0}') #清理商铺权重
        #正则保存商品各项指标
        title = re.findall(r'"raw_title":"([^"]+)"',resp_text_raw_title,re.I) #正则保存商品名称
        nid = re.findall(r'"nid":"([^"}]+)"',resp_text_nid,re.I) #正则保存商品id
        category = re.findall(r'"category":"([^"}]+)"',resp_text_category,re.I) #正则保存商品类别
        price = re.findall(r'"view_price":"([^"]+)"',resp_text_view_price,re.I) #正则保存商品价格
        sales = re.findall(r'"view_sales":"([^"]+)"',resp_text_view_sales,re.I) #正则保存商品销量
        comment = re.findall(r'"comment_count":"([^"]+)"',resp_text_comment_count,re.I) #正则保存评论数
        nick = re.findall(r'"nick":"([^"]+)"',resp_text_nick,re.I) #正则保存商户名称
        nick = nick[0:len(nick)-1] #页面底部会多出一个空白的nick属性，这里要去掉
        user_id = re.findall(r'"user_id":"([^"]+)"',resp_text_user_id,re.I) #正则保存商户id
        loc = re.findall(r'"item_loc":"([^"]+)"',resp_text_item_loc,re.I) #正则保存商户地址
        tmail = re.findall(r'"isTmall":([^",]+)',resp_text_isTmall,re.I) #正则保存是否是天猫
        sellercredit = re.findall(r'"sellerCredit":([^",]+)',resp_text_sellerCredit,re.I) #正则保存是商户信用
        totalrate = re.findall(r'"totalRate":([^"}]+)',resp_text_totalRate,re.I) #正则保存店铺权重，天猫为10000满分
        x_1 = len(title) #每一页商品的数量，也即该轮采集的末位索引
        index_df = [] #清空索引
        title_df = [] #清空商品名称
        nid_df = [] #清空商品id
        category_df = [] #清空商品类别
        price_df = [] #清空价格
        sales_df = [] #清空销量
        comment_df = [] #清空商品评论
        nick_df = [] #清空商户名称
        user_id_df = [] #清空商户id
        loc_df = [] #清空商户地址
        tmail_df = []#清空天猫属性
        sellercredit_df = [] #清空卖家信用
        totalrate_df = [] #清空商铺权重
        merge = [] #清空上一轮的采集结果
        for i in range(x_0,x_0+x_1): #创建本轮索引
            index_df.append(i)
        x_0 = x_0 + x_1 #创建下一轮采集的首位索引
        title_df = pd.DataFrame(title,index=index_df,columns=['title']) #将商品名称dataframe化
        nid_df = pd.DataFrame(nid,index=index_df,columns=['nid']) #将商品id dataframe化
        category_df = pd.DataFrame(category,index=index_df,columns=['category']) #将商品类别dataframe化
        price_df = pd.DataFrame(price,index=index_df,columns=['price']) #将价格dataframe化
        sales_df = pd.DataFrame(sales,index=index_df,columns=['sales']) #将销量dataframe化
        comment_df = pd.DataFrame(comment,index=index_df,columns=['comment']) #将评论dataframe化
        nick_df = pd.DataFrame(nick,index=index_df,columns=['nick']) #将商户名称dataframe化
        user_id_df = pd.DataFrame(user_id,index=index_df,columns=['user_id']) #将商户id dataframe化
        loc_df = pd.DataFrame(loc,index=index_df,columns=['loc']) #将商户地址dataframe化
        tmail_df = pd.DataFrame(tmail,index=index_df,columns=['tmail']) #将天猫属性dataframe化
        sellercredit_df = pd.DataFrame(sellercredit,index=index_df,columns=['sellercredit']) #将卖家信用dataframe化
        totalrate_df = pd.DataFrame(totalrate,index=index_df,columns=['totalrate']) #将商铺权重dataframe化
        merge = [title_df,nid_df,category_df,price_df,sales_df,comment_df,nick_df,user_id_df,loc_df,tmail_df,
        sellercredit_df,totalrate_df] #合并本轮采集结果
        merge = pd.concat(merge,axis=1) #将本轮采集结果dataframe化
        print('..第'+str(k+1)+'页已解析完成')
        if k == 0: #若为首轮采集，则采集集合即为本轮（首轮）采集结果
            merge_accumulation = merge
        elif k > 0: #若不是首轮采集，则将本轮采集的结果从采集集合的末尾处合并
            merge_accumulation = [merge_accumulation, merge]
            merge_accumulation = pd.concat(merge_accumulation,axis=0)
        print('..第'+str(k+1)+'页已聚合完成')
        if k + 1 < numberofpages: #若执行完循环过程，则需继续延迟并检查ip使用情况
            time.sleep(random.randrange(0,maxdelay*100,1)/100) #在给定时间范围内随机延迟
            changeip() #判断当前ip的循环次数是否大于等于允许的最大值，若超过则更换ip
    date = time.strftime("%Y%m%d%H%M%S", time.localtime()) #获取当前日期和时间
    date_path = merge_path + date + csvname #构建含日期的保存路径
    merge_accumulation.to_csv(date_path) #保存采集集合至csv文件
    print('采集全部完成，将结果保存至csv文件')
    #winsound.Beep(300, 10000) #爬虫运行结束后发出提示音
    return merge_accumulation

for target in target_list:
    ip_list = get_ip_list(url, headers=headers) #获取代理ip
    proxies = get_random_ip(ip_list) #定义proxies为从ip_list中随机选取的一个ip地址
    payload = {'q': target,'s': '1','ie':'utf8','sort': 'sale-desc'}  #通过字典传递url参数，q为商品名称
    merge_path = 'F:/python_workshop/pachong/' + target #设置保存路径和文件名
    getdata(url_target,payload,numberofpages,maxiploops,merge_path) #运行爬虫
    print('关键词' + target + '已采集完成')


#os.system("shutdown -s -t 0")


