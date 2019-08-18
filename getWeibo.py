#! usr/bin/env python3
# -*- coding: utf-8 -*-

#Usage:
#	auto download the json of all your weibo
# 	change url for different users
#	change range of pages for different ranges
#	refer to the top answer in https://www.zhihu.com/question/20339936
import time
import random
import requests

url='' # 参考上面的知乎答案拿到链接，getIndex....page=
for i in range(1, 772):	# 一页10条微博，自己算
	print("Getting page " + str(i))

	time.sleep(random.random() + random.randint(2, 4))
	res = requests.get(url+str(i))

	with open('result/' + str(i) + '.json', 'w') as f:
		f.write(res.text)
	time.sleep(1)

print("Done.")