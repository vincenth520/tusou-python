#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-05 19:01:25
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$
import os,random
import sys
if __name__ == '__main__':
	import url_manager,html_downloader,html_parser
else:
    from . import url_manager,html_downloader,html_parser

class Gather(object):
	"""
		图片采集
	"""
	def __init__(self, s):
		self.search = s
		self.pic_path = set()
		self.urls = url_manager.UrlManager(self.search)
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser(self.search)
		self.root_url = 'http://www.topit.me/items/search?query=' + self.search +'&p='+str(random.randint(2,10))
		#print(self.parser.set_path())
		if os.path.exists(self.parser.set_path()):
			print('目录存在')
		else:
			os.makedirs(self.parser.set_path())


	def craw(self):
		count = 1
		self.urls.add_new_url(self.root_url)
		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()
				print('craw %d:%s' %(count,new_url))
				html_cont = self.downloader.download(new_url)
				#print(html_cont)
				new_urls,new_data_path = self.parser.parse(new_url,html_cont)
				for data in new_data_path:
					self.pic_path.add(data)	
				self.urls.add_new_urls(new_urls)
				#self.outputer.collect_data(new_data)
				if count == 10:
					break
				count = count + 1
			except Exception as ex: 
				print (Exception,"[__init__.py]:",ex)

		return self.pic_path



if __name__ == '__main__':
	#root_url = 'http://www.topit.me/items/search?query=d' 
	obj_spider = Gather('美女')
	print(obj_spider.craw())