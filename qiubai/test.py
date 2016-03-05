# coding=utf-8


from bs4 import BeautifulSoup
soup = BeautifulSoup(open("新浪首页.html")) #新浪首页的源代码
soup2 = BeautifulSoup(open("view-source_www.sina.com.cn.html")) #新浪首页源代码页面的源代码

for element in soup.find_all("a"):
    if len(element.contents) > 0:
        print element.contents[0].encode("utf-8") # contents是list，所以需要先slice才行
    if "href" in element.attrs:
        print "href: ", element["href"].encode("utf-8")



print "hello, world"
