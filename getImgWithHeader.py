import os

import requests
from bs4 import BeautifulSoup

# 浏览器请求头（大部分网站没有这个请求头会报错）
headers = {'Accept': '*/*',
           'Accept-Language': 'en-US,en;q=0.8',
           'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive',
           'Referer': 'http://www.mzitu.com/'
           }

all_url = 'http://www.mzitu.com/xinggan/'
"""
1. 请求的初始界面
"""
start_html = requests.get(all_url, headers=headers).content.decode('utf-8')
"""
2. 获取最大页面数，因为按钮的连接都在class是nav-links的div下
"""
Soup = BeautifulSoup(start_html, 'lxml')  # BeautifulSoup是一个可以从HTML或XML文件中提取数据的Python库
all_a = Soup.find('div', class_='nav-links').find_all("a")[-2].get_text()  # 意思是先查找 class为 all 的div标签，然后查找所有的<a>标签。
# print(all_a)
for page in range(1, int(all_a) + 1):
    """
    3. 循环模拟每个页面的请求
    """
    page_url = all_url + 'page/' + str(page) + "/"
    page_html = requests.get(page_url, headers=headers).content.decode('utf-8')

    mpage_scop = BeautifulSoup(page_html, 'lxml')
    """
    4. 获取每个页面图集的链接
    """
    page_html_html = mpage_scop.find('ul', id='pins').find_all('a')  # .find_all("a")[-2].get_text()
    print("==========>", page_html_html)
    for a in page_html_html:
        tu_href = a['href']  # 取出a标签的href 属性

        title = a.get_text()  # 取出a标签的文本
        path = str(title).strip()
        if path != '':
            """
            5. 伪造不同的Referer，不然为网站会以为是盗链的
            """
            headerstwo = {'Accept': '*/*',
                          'Accept-Language': 'en-US,en;q=0.8',
                          'Cache-Control': 'max-age=0',
                          'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                          'Connection': 'keep-alive',
                          'Referer': tu_href
                          }
            # 因为目录不能包含以下特殊字符 否则会报错
            path = path.replace(":", "")
            path = path.replace("?", "")
            path = path.replace("？", "")
            path = path.replace("\\", "")
            path = path.replace("\/", "")
            path = path.replace("*", "")
            path = path.replace("'", "")
            path = path.replace("\"", "")
            path = path.replace("<", "")
            path = path.replace(">", "")
            path = path.replace("|", "")
            print("=========", path)
            """
            6. 创建一个存放套图的文件夹并进入
            """
            os.makedirs(os.path.join("D:\doc\images\pachong", path))
            os.chdir("D:\doc\images\pachong\\" + path)

            """
            7. 请求套图链接，同样获取套图最大页数
            """
            tu_html = requests.get(tu_href, headers=headerstwo).content.decode('utf-8')
            tu_scop = BeautifulSoup(tu_html, 'lxml')
            tu_html = tu_scop.find('div', class_='pagenavi').find_all("a")[-2].get_text()
            # print(tu_html)
            for tu_real in range(1, int(tu_html) + 1):
                each_url = tu_href + '/' + str(tu_real)
                print(each_url)
                """
                7. 请求套图中每个页面，获取页面下的图片路径
                 """
                each_html = requests.get(each_url, headers=headerstwo).content.decode('utf-8')
                img_Soup = BeautifulSoup(each_html, 'lxml')
                img_url = img_Soup.find('div', class_='main-image').find('img')['src']
                # print(img_url)
                name = img_url[-9:-4]  ##取URL 倒数第九至第四位 做图片的名字
                """
                8. 请求图片，创建jpg文件并将对应名称图片写入
                """
                img = requests.get(img_url, headers=headerstwo)
                f = open(name + '.jpg', 'ab')  ##写入多媒体文件必须要 b 这个参数！！必须要！！
                f.write(img.content)  ##多媒体文件要是用conctent哦！
                f.close()
