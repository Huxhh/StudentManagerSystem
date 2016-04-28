# -*- coding: utf-8 -*-
import MySQLdb as mysql
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash


db = mysql.connect(host = '127.0.0.1', user = 'root', passwd = '563255387', db = 'studentmanagersystem', charset = 'utf8')

db.autocommit(True)
cursor = db.cursor()

app = Flask(__name__)
app.config.from_object(__name__)


if __name__ == '__main__':
    app.run()
