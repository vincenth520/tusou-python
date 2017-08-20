#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-05 19:02:14
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$
from bs4 import BeautifulSoup
import time,uuid
import html_downloader
import re

class HtmlParser(object):
	
	def _get_new_urls(self,page_url,soup):
		new_urls = set()
		links = soup.find_all('a',href=re.compile(r'http://www.topit.me/item/\w+'))
		for link in links:
			new_urls.add(link['href'])
		return new_urls

	def _get_new_data(self,page_url,soup):
		#img admin_collection ui-draggable
		try:
			img = soup.find('img',class_='admin_collection')
			id = 'img/%015d%s000.jpg' %(int(time.time() * 1000),uuid.uuid4().hex)
			downloader = html_downloader.HtmlDownloader()
			pic = downloader.download(img['src'])
			f = open(id,'wb')
			f.write(pic)
			f.close()
			return True
		except:
			return False

	def parse(self,page_url,html_cont):
		if page_url is None or html_cont is None:
			return

		soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
		new_urls = self._get_new_urls(page_url,soup)
		new_data = self._get_new_data(page_url,soup)
		return new_urls
		
