#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-07 16:46:00
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$

import os,random,json,threading,zipfile,base64,urllib.parse
from flask import Flask
from flask import request,redirect,url_for,send_from_directory,make_response
from flask import render_template
from gather import Gather
import BloomFilter
import db_inc

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
bloomfilter = BloomFilter.BloomFilter()

# 首页
@app.route('/')
def index():
	list = getpiclist(20)
	return render_template('index_page.html',piclist=json.loads(list),title='图搜 - 一个强大的在线图库搜索',hot=hot(5,'click desc'))

#首页获取推荐图片
@app.route('/api/getpiclist/<num>')
def getpiclist(num):
	num = int(num)
	piclist = set()
	files = os.listdir('./static/tmp/')
	random.shuffle(files)
	for d in files:
		if num == 0:
			break
		if(file_extension(d) == '.jpg'):
			piclist.add(setUrl()+'/static/tmp/'+d)
		num = num - 1
	return json.dumps(list(piclist))

# API获取search list
@app.route('/api/search/<s>')
def searchlist(s):

	t = threading.Thread(target=searchshell, args=(s,))
	t.start()
	t.join()
	print('这里',t)
	#old_piclist = set()
	piclist = set()
	files = os.listdir('./static/tmp/'+s)
	#print(old_piclist,'zhege')
	#random.shuffle(files)
	for d in files:
		if(file_extension(d) == '.jpg'):  
			piclist.add(setUrl()+'/static/tmp/'+s+'/'+d)
			#old_piclist.add(setUrl()+'/static/tmp/'+s+'/'+d)
			#print('piclist',setUrl()+'/static/tmp/'+s+'/'+d)
	return json.dumps(list(piclist))

# def getsearchlist(s):
# 	pass

# 执行爬取脚本
#@app.route('/shell/api/search/<s>')
def searchshell(s):
	gather = Gather(s)
	piclist = gather.craw()
	return json.dumps(list(piclist))

# 搜索图片界面
@app.route('/search/<s>')
def search(s):
	db = db_inc.get_db()
	cur = db.cursor()
	rs = db_inc.query_db('select * from search where name = \''+s+'\'')
	print('长度',len(rs))
	if(len(rs) == 0):
		cur.execute('insert into search(id,name,click) values(null,\''+s+'\',1)')
	else:
		cur.execute('update search set click = click+1 where name = \''+s+'\'')
	#print(cur.rowcount)
	# for user in db_inc.query_db('select * from search'):
	# 	print (user['id'], 'has the id', user['name'])
	cur.close()
	db.commit()
	db.close()
	# cur.execute('select * from search')
	# value = cur.fetchall()
	# print('这是',value)
	path = './static/tmp/'+s
	# resp = make_response(render_template(...))
	# resp.set_cookie('this_path', path)
	#print(path)
	piclist = set()
	if os.path.exists(path):
		i = 0
		files = os.listdir(path)
		for d in files:
			if i == 20:
				break
			if(file_extension(d) == '.jpg'):
				piclist.add(path[1:]+'/'+d)
				i = i + 1
		#piclist = searchlist(s)
		piclist=json.dumps(list(piclist))
	else:
		pass
		piclist = searchshell(s)
	return render_template('search_page.html',piclist=json.loads(piclist),s=s)


# 单图片页面
@app.route('/pic')
def pic():
	pic = urllib.parse.unquote(request.args.get('item'))
	if os.path.exists(pic.replace(setUrl(),'./')):
		return render_template('pic.html',pic=pic,hot=hot(10,'click desc'),rand=hot(1,'RANDOM()'))
	return page_not_found(404)


# 获取最热搜索词
def hot(num,type):
	db = db_inc.get_db()
	cur = db.cursor()
	hotsearch = db_inc.query_db('select * from search order by '+type+' limit '+str(num))
	return hotsearch

# 404页面
@app.errorhandler(404) 
def page_not_found(error): 
	return render_template('404.html'), 404 

# 设置域名
def setUrl():
	return 'http://localhost:5000'

# 获取文件后缀
def file_extension(path): 
	return os.path.splitext(path)[1]


# @app.route('/baseget/<s>')
# def safe_base64_decode(s):
# 	a = (-len(s)) % 4
# 	s=s+'='*a
# 	return base64.b64decode(urllib.parse.quote(s)).decode()

# @app.route('/base')
# def safe_base64_encode():
# 	return base64.b64encode(request.args.get(urllib.parse.unquote('s')).encode(encoding="utf-8")).decode().replace('=','')


if __name__ == '__main__':
	#app.debug = True
	app.run(host='0.0.0.0')