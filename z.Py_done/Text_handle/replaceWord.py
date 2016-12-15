python 字符串替换

python 字符串替换是python操作字符串的时候经常会碰到的问题，这里简单介绍下字符串替换方法。

python 字符串替换可以用2种方法实现:
1是用字符串对象本身的方法。
2用正则来替换字符串

下面用个例子来实验下：
a = 'hello word'
我把a字符串里的word替换为python

1用字符串本身的replace方法
a.replace('word','python')
输出的结果是hello python

2用正则表达式来完成替换:
import re
strinfo = re.compile('word')
b = strinfo.sub('python',a)
print b
输出的结果也是hello python