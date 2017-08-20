#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-05 19:01:25
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$
import os
from urllib import parse
if __name__ == '__main__':
	import html_parser,BloomFilter
else:
    from . import html_parser,BloomFilter

class UrlManager(object):
	
	def __init__(self,s):
		self.search = s
		self.new_urls = set()
		self.old_urls = set()
		self.parser = html_parser.HtmlParser(self.search)
		self.bloomfilter = BloomFilter.BloomFilter()
		self.list_path = os.getcwd()+'/static/old_url/'+self.search+'.txt'
		#print(self.search,'sdasda')
		if os.path.exists(self.list_path):
			pass
		else:
			tmp = open(self.list_path,'w')
			tmp.close()

		fd = open(self.list_path,'r')  
		while True:   
			url = fd.readline()  
			if (url > '') - (url < '') == 0: #if url is equal exit break  
				break  
			#print(url)
			self.old_urls.add(url.replace('\n','')) 
		fd.close() 
		print(self.old_urls)

	def add_new_url(self,url):
		if url is None:
			return

		if url not in self.new_urls and url not in self.old_urls:
			url = url.replace(self.search,parse.quote(self.search))
			# if self.bloomfilter.isContaions(url) == False:  
			# 	self.bloomfilter.insert(url) 
			# print(url,'sada')
			# fd = open(self.list_path,'a+')
			self.new_urls.add(url)
			# fd.write(url+'\n')
			# fd.close()
	
	def add_new_urls(self,urls):
		if urls is None or len(urls) == 0:
			return
		for url in urls:
			self.add_new_url(url)

	def has_new_url(self):
		return len(self.new_urls) != 0

	def get_new_url(self):
		new_url = self.new_urls.pop()
		self.old_urls.add(new_url)
		fd = open(self.list_path,'a+')
		fd.write(new_url+'\n')
		fd.close()
		return new_url