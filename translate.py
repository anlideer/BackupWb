#! usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import re

def removeHtml(text):
	origin = text
	origin = re.sub('<a.*?>', '', origin)
	origin = re.sub('</a>', '', origin)
	origin = re.sub('<br />', '', origin)
	origin = re.sub('<span.*?>', '', origin)
	origin = re.sub('</span>', '', origin)
	origin = re.sub('<img.*?>', '', origin)
	return origin


def proceed(content, fout):
	items = json.loads(content)['data']

	if 'cards' not in items:
		return
	
	for card in items['cards']:
		if 'mblog' not in card:
			continue

		mblog = card['mblog']
		name = mblog['user']['screen_name']
		time = mblog['created_at']
		mfrom = mblog['source']

		# basic info
		fout.write(name + " " + time + " " + mfrom + '\n')
		# text
		whole = []
		origin = mblog['text']
		se = re.search('(<a href=\\"/status/[0-9]*?\\">)', origin)
		if se:
			whole.append(se.group())
		origin = removeHtml(origin)
		fout.write(origin + '\n')
		# pics
		pics = []
		if 'pics' in mblog:
			for pic in mblog['pics']:
				if 'large' in pic:
					pics.append(pic['large']['url'])
				else:
					pics.append(pic['url'])
		# if repost: repo text
		if "retweeted_status" in mblog and mblog['retweeted_status']['user']:
			repouser = mblog['retweeted_status']['user']['screen_name']
			repotime = mblog['retweeted_status']['created_at']
			repotext = mblog['retweeted_status']['text']
			se = re.search('(<a href=\\"/status/[0-9]*\\">)', repotext)
			if se:
				whole.append(se.group())
			repotext = removeHtml(repotext)
			fout.write("repost from: \n")
			fout.write(repouser + " " + repotime + '\n')
			fout.write(repotext + '\n')
			if 'pics' in mblog['retweeted_status']:
				for pic in mblog['retweeted_status']['pics']:
					if 'large' in pic:
						pics.append(pic['large']['url'])
					else:
						pics.append(pic['url'])

		if pics:
			fout.write("pics src:\n")
			fout.writelines(pics)
			

		if whole:
			fout.write("see whole text:\n")
			for w in whole:
				realUrl = 'm.weibo.cn/status/'
				number = re.search('(\d+)', w)
				if number:
					realUrl += number.group()
				realUrl += '/'
				fout.write(realUrl + '\n')


		
		fout.write('\n\n')




for i in range(1, 768): # 根据微博条数除以10自己调整一下
    content = open('result/%d.json' % i).read()
    fout = open('weibo/%d.txt' % i, 'w', encoding = 'utf-8')
    try:
    	proceed(content, fout)
    except:
    	print("error" + str(i))
    finally:
    	fout.close()


print("Done.")