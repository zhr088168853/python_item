import requests                     #导入爬虫所需的requests库
import re                                #导入正则表达式库
import os                                #导入操作系统库

def getHTMLText(url):           #获取网页页面函数，根据对应的url获取对应的网页页面，可根据url获取多个页面
    try:
        kv = {                                                                          #反爬技术：定义字典类型的请求头，需要有cookie和user-agent，原因是淘宝实施了反爬虫机制，需要模拟浏览器访问的方式进行爬取，则需要加上字典kv
        "cookie": "mt=ci%3D-1_0; miid=1526854784567691282; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tracknick=tb929500154; _cc_=W5iHLLyFfA%3D%3D; tg=0; cna=Ow+gElPqiTgCAQ7SAC5TvHQS; _uab_collina=158132578816374262338523; enc=ecWrrisVMs0AwLI0kXDIZt1IdMoC73jpy%2FpNWjtXU2JrAlKPbIqz%2B4Myyxcj50PLX8udaE2dbN0PwIRRLLAJQPt2CUok88HhKvGTXmOywZ0%3D; cookie2=1090efabb528573d413bbc385a5418b1; t=1458be1fd6e3a995b6881340fb908e03; _tb_token_=33b73087a7513; _samesite_flag_=true; v=0; UM_distinctid=172a7c442e124-0514aa7e5e3742-376b4502-100200-172a7c442e2230; JSESSIONID=786F5FDDDCD58D6F38CE5E8616833EE7; l=eBSMGig4q2t3QikSBOfanurza779IIRYnuPzaNbMiOCPO2fpSyh1WZxSnZY9CnhVh65eR3rEQAfvBeYBqIv4n5U62j-la_Hmn; isg=BBAQzmQVenYwkyUI-89BQ29T4V5i2fQjBcmwSArh32syRbDvsuqss4p3GA2lr6z7",
        "user-agent": "Mozilla/5.0 "}                                     #在发送请求时设置user-agent头，将user-agent的值设置为真实浏览器发送请求的user-agent
        r = requests.get(url, headers=kv, timeout=30)       #根据对应的url获取对应的网页页面,加入请求头参数，设置获取网页的时间不超过30秒
        r.raise_for_status()                                                      #检查返回的状态码是否为200
        r.encoding = r.apparent_encoding                           #将网页编码方式设置为utf-8
        return r.text                                                                #返回获取到的网页
    except:                                                                            #若返回的状态码不是200，则提示获取失败的信息
        print("网页获取失败")


def getParsePage(info, image_list, html):                                #将获取到的网页页面进行解析并提取关键信息和商品图片链接，分别保存在两个列表中
    try:
        price = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)       #用正则表达式获取含有商品价格的信息
        goods_name = re.findall(r'\"raw_title\"\:\".*?\"', html)   #用正则表达式获取含有商品名称的信息
        shop_name = re.findall(r'\"nick\":\".*?\"', html)              #用正则表达式获取含有店铺名称的信息
        location = re.findall(r'\"item_loc\":\".*?\"', html)            #用正则表达式获取含有店铺地点的信息
        sales = re.findall(r'\"view_sales\":\".*?\"', html)              #用正则表达式获取含有商品销量的信息
        image = re.findall(r'\"pic_url\"\:\".*?\"', html)                 #用正则表达式获取含有商品图片链接的信息
        for i in range(len(price)):
            goods_price = eval(price[i].split(':')[1])                         # 提取商品价格
            goods_sales = eval(sales[i].split(':')[1])                         # 提取商品销量
            shopname = eval(shop_name[i].split(':')[1])                 # 提取店铺名称
            local = eval(location[i].split(':')[1])                                # 提取店铺地点
            title = eval(goods_name[i].split(':')[1])                          # 提取商品名称
            image_url = eval(image[i].split(':')[1])                           # 提取商品的图片链接
        
            info.append([goods_price, goods_sales, shopname, local, title])         #分别将商品的各项信息存储在列表中
            image_list.append(image_url)                                                                #将商品的图片链接存储在列表中
    except:                                                                                                             #若商品信息提取不到，则提示提取失败的信息
        print("商品信息提取失败")

def get_image(image_list):                                  #根据得到的商品图片链接获取对应的图片
    print("正在爬取商品图片，请稍候……\n")
    i = 0                                                                  #定义变量i，用于确定图片的名称
    root="D:\\picture\\"                                        #定义图片存储的根目录
    for url in image_list:
        i = i + 1                                                         #每获取到一个图片链接，i自增1
        url="http:"+url                                             #下载图片的完整url
        path=root+str(i)+"."+url.split(".")[-1]         #将url的最后一个 ' . ' 后的字符串获取出来（即jpg）再与root连接起来构成图片存储的完整地址

        try:
            if not os.path.exists(root):                        #若根目录不存在,则创建根目录
                os.mkdir(root)                                       #创建根目录
                r=requests.get(url)                               #下载商品图片
                with open(path,"wb") as f:
                    f.write(r.content)                              #将图片保存到D盘的picture文件夹中
                    f.close()                                             #关闭文件流
            else:                                                           #若根目录已存在，则直接下载商品图片
                r=requests.get(url)                               #下载商品图片
                with open(path,"wb") as f:
                    f.write(r.content)                              #将图片保存到D盘的picture文件夹中
                    f.close()                                             #关闭文件流
        except:                                                          #若商品图片爬取不到，则进入下一轮的爬取
            continue                                       
    return 1                                                             #爬取完成返回1
    


def save_goods_msg(ilt):                                                                  #将得到的关键信息保存在文件中，并进一步作词频统计
    try:
        f = open("D:\\goods_msg.csv","w", encoding = "utf-8")        #将商品信息保存到goods_msg.csv文件中
        f1 = open("D:\\word.txt", "w", True, "utf-8")                           #将待统计的店铺地点信息保存到word.txt文件中
        
        f.write("序号,价格,销量,店铺名称,店铺地点,商品名称\n")             #写入表头
        count = 0                                                                                   #定义count变量，用于统计爬取的商品总数
        for g in ilt:
            s = ""                                                                                      #定义一个空字符串，用于字符串拼接
            count += 1                                                                            #统计爬取的商品总数
            f.write(str(count) +','+ g[0] +','+ g[1] +','+ g[2] +','+ g[3] +','+ g[4]+'\n')    #将商品信息保存在CSV文件中，用逗号分隔值
            list1 = g[3].split(" ")                                                                                           #对于每一个店铺地点，其字符串中间有一个空格，所以以空格切割
            s = s.join(list1)                                                                                                   #将切割字符串得到的字符串列表转换为字符串
            if count != len(ilt):                                                                                             #若未到最后一个关键词，则附带写入一个空格，空格为了分隔每个关键词  
                f1.write(s+" ")                                                                                                #将关键词和空格写入文件
            else:                                                                                                                    #若到最后一个关键词，则只写入关键词，不写入空格
                f1.write(s)                                                                                                       #将关键词写入文件
        f.close()                                                                                                                   #关闭文件流
        f1.close()                                                                                                                 #关闭文件流
        print("一共有{}个商品, 商品信息已保存在D:\\goods_msg.csv文件中\n".format (count))     #输出爬取商品的总数和保存文件的信息
        print("店铺地点的关键词语已保存在D:\\word.txt文件中\n")                                                 #输出保存文件的信息
        countword()                     #调用函数，做词频统计
        return 1                            #若以上操作无异常，则返回1
    except:                                 #若在爬取时有应用打开word.csv文件，则保存商品信息失败，返回0，应在爬取信息完成后再打开文件查看
        return 0
    
    
def countword():                                                             #词频统计函数
    word_lst = []                                                               #定义一个列表，用于存储文件内容形成的列表
    word_dict= {}                                                              #定义一个字典，用于存储统计的关键词
    count = 0                                                                    #定义count变量，用于统计关键词语的总数
    with open('D:\\word.txt',"r", True, "utf-8") as wf, open('D:\\count_result.txt',"w", True, "utf-8") as wf2:     #打开word.txt和count_result.txt两个文件
        for word in wf:    
            word_lst.append(word.split(" "))                        #去除文件中的空格，得到一个列表，再将此列表加入word_lst列表中
            for item in word_lst:                                           #将word_lst列表中每一个列表元素取出来
                for item2 in item:                                            #将列表元素中的每一个值取出来
                    if item2 not in word_dict:                           #若列表元素的值在word_dict中找不到，则统计第一次
                        word_dict[item2] = 1                              #统计关键词的数目
                        count+=1                                                #count变量自增1
                    else:                                                             #若列表元素的值在word_dict中已存在，则累加统计
                        word_dict[item2] += 1                           #累加统计关键词的数目
                        count+=1                                                #count变量自增1
        print("店铺地点的关键词语总数为{}，词频统计如下：".format (count))                  #输出统计的关键词总数
        print("店铺地点的关键词语总数为{}，词频统计如下：".format (count), file=wf2)
        for key in word_dict:
            print (key,word_dict[key], sep='------')                                                             #输出关键词的统计结果
            wf2.write(key+' '+str(word_dict[key]) + "\n")                                                  #将关键词的统计结果保存在文件中以便查看
        print("\n词频统计结果成功保存在D:\\count_result.txt中！")

def main():
    goods = input("请输入商品名称（如手机）：")                              #输入待获取的商品名称
    depth = input("请输入爬取商品的页数：")                                     #输入需爬取商品的页数
    print("\n正在爬取商品信息，请稍候……\n")                                    # 提示正在获取商品的信息
    start_url = 'https://s.taobao.com/search?q=' + goods               #爬取网站的主要链接
    infoList = []                                                                                     #定义列表用于存储商品的各项信息
    image_list=[]                                                                                   #定义列表用于存储初始获取到的商品图片链接
    for i in range(int(depth)):                                                                #根据需爬取商品的页数循环爬取
        try:
            url = start_url + '&s=' + str(44 * i)                                         #获取到爬取各页商品的完整链接
            html = getHTMLText(url)                                                       #调用函数，根据对应的url获取对应的网页页面
            getParsePage(infoList, image_list, html)                               #调用函数，将获取到的网页页面进行解析并提取关键信息和商品图片链接，分别保存在两个列表中
        except:
            continue                                                                                   # 若有商品爬取不到则进入下一轮爬取
    if get_image(image_list):                                                                 #调用函数，根据得到的商品图片链接获取对应的图片，若图片下载成功则提示相应信息
        print("商品图片成功保存在D:\\picture中\n")                                     
    if not save_goods_msg(infoList):                                                     #调用函数，将得到的关键信息保存在文件中，并进一步作词频统计
        print("您正在打开文件，请关闭word.csv文件再重新爬取")            #若在爬取时有应用打开word.csv文件，则无法保存相应的商品信息，需关闭word.csv文件再重新爬取
    else:
        print("\n爬取成功！")                                                                    #成功将商品信息保存

if __name__ == '__main__':
    main()

