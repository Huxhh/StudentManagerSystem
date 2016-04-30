# -*- coding: utf-8 -*-
import MySQLdb as mysql
import logging
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response
from models import DBSession, Admin, Student
from responsebody import ResponseBody


# db = mysql.connect(host = '127.0.0.1', user = 'root', passwd = '563255387', db = 'studentmanagersystem', charset = 'utf8')

# db.autocommit(True)
# cursor = db.cursor()

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def login():
    username = request.cookies.get('username')
    if username is None:
        return render_template('login.html')
    else:
        return render_template('showStudent.html')


@app.route('/auth')
def authenticate():
    session = DBSession()
    username = request.form['username']
    password = request.form['password']
    try:
        result = session.query(Admin).filter(Admin.name == username and Admin.password == password).one()
        if result is None:
            logging.info('No such Administrator')
            return render_template('login.html')
        else:
            resp = make_response(render_template('showStudents.html'))
            resp.set_cookie('username', 'username')
    except Exception as e:
        logging.info(e)
        print e
    finally:
        session.close()


@app.route('/showStudents/<pageindex>')
def showstudents(pageindex = 1):
    session = DBSession()
    try:
        students = session.query(Student).pagintion(pageindex, 5, False)
        return ResponseBody(1, students).getContent()
    except Exception as e:
        logging.info(e)
        print e
    finally:
        session.close()


@app.route('/manage/addStudent')
def addstudent():
    session = DBSession()
    name = request.form['name']
    no = request.form['studentno']
    phone = request.form['phonenumber']
    email = request.form['studentemail']
    try:
        session.execute(Student, sname = name, sno = no, sphone = phone, semail = email)
    except Exception as e:
        logging.info(e)
        print e
    finally:
        session.close()


@app.route('/manage/deleteStudent/<sno>')
def deletestudent(sno):
    session = DBSession()
    try:
        session.delete(Student, sno = sno)
    except Exception as e:
        logging.info(e)
        print e
    finally:
        session.close()


@app.route('/manage/editStudent/<sno>')
def editstudent(sno):
    session = DBSession()
    name = request.form['name']
    no = request.form['studentno']
    phone = request.form['phonenumber']
    email = request.form['studentemail']
    try:
        student = session.query.get_by(sno = sno)
        student.sname = name
        student.sno = no
        student.sphone = phone
        student.semail = email
        session.flush()
    except Exception as e:
        logging.info(e)
        print e
    finally:
        session.close()


if __name__ == '__main__':
    app.run()
