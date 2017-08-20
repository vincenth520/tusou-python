#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-09 22:41:51
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$

from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash, _app_ctx_stack

DATABASE = 'pic.db'
DEBUG = True
SECRET_KEY = 'husngc8643ms5!./^hsj'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#初始化数据库
def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('pic.sql') as f:
            db.cursor().executescript(f.read().decode())
        db.commit()


def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()

if __name__ == '__main__':
    init_db()
    #app.run()