# -*- coding: utf-8 -*-
# __author__ = 'Administrator'
"""

"""
from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>菜鸟教程(runoob.com)</title>
</head>
<body>
    <h1>我的第一个标题</h1>
    <p class ="c_class" name ="c_name" style="width:50px;border:1px">我的第一个段落。</p>
    <a href="http://baidu.com">click here</a>
        <a href="http://baidu.com">clickdddd here</a>
</body>
</html>
"""

soup = BeautifulSoup(html, "lxml")

print(soup.prettify())
print("1--------------------")
print(soup.title)
print("2--------------------")
print(soup.head)
print("3--------------------")
print(soup.a)
print("4--------------------")
print(type(soup.a))
print("5--------------------")
print(soup.name)
print("6--------------------")
print(soup.head.name)
print("7--------------------")
print(soup.p.attrs)
print("8--------------------")
print(soup.p["class"])
print(soup.p.get("class"))
print("9--------------------")
print(soup.p)
soup.p["class"] = "newclass"
print(soup.p)
print("10--------------------")