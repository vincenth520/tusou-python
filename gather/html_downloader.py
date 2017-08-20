#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-05 19:01:47
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$

from urllib import request,parse

class HtmlDownloader(object):
	
	def download(self,url):
		if url is None:
			return None
		try:
			req = request.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36')
			req.add_header('Referer',url)
			req.add_header('Cookie','PHPSESSID=lsjom1i32131crbh4mnl579rh6; request_url=%2F; is_click=1; item-tip=true; tip_global_1=true; Hm_lvt_5256b9d21d9d68644fca1a0db29ba277=1459853520; Hm_lpvt_5256b9d21d9d68644fca1a0db29ba277=1459853541')
			#print(url)
			response = request.urlopen(req)
			#print(url)

			if response.getcode() != 200:
				return None

			# f = open('test.html','wb')
			# f.write(response.read())
			# f.close()
			#print(url)
			return response.read()
		except Exception as ex: 
			print (Exception,":[html_downloader.py]",ex  )
