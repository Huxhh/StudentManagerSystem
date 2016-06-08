# -*- coding: utf-8 -*-
import MySQLdb as mysql
import logging
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, json
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


@app.route('/signout')
def signout():
    request.cookies.delete('username')
    return render_template('login.html')


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
        return ResponseBody(1, None)()
    finally:
        session.close()


@app.route('/showStudents/<pageindex>')
def showstudents(pageindex = 1):
    session = DBSession()
    try:
        students = session.query(Student).all()#.pagination(pageindex, 5, False)
        list = []
        students[0].to_dict()
        for i in students:
            list.append(i.to_dict())
        return ResponseBody(0, list).getContent()
    except Exception as e:
        logging.info(e)
        print e
        return ResponseBody(1, None)()
    finally:
        session.close()


@app.route('/manage/addStudent', methods=['POST'])
def addstudent():
    session = DBSession()
    name = request.form['name']
    no = request.form['studentno']
    phone = request.form['phonenumber']
    email = request.form['studentemail']
    try:
        student = Student(name, no, phone, email)
        session.add(student)
        return ResponseBody(0, None).getContent()
    except Exception as e:
        logging.info(e)
        print e
        return ResponseBody(1, None)()
    finally:
        session.commit()
        session.close()


@app.route('/manage/deleteStudent/<sid>', methods=['POST'])
def deletestudent(sid):
    session = DBSession()
    try:
        student = session.query(Student).filter(Student.id == sid).one()
        session.delete(student)
        session.commit()
        return ResponseBody(0, None)()
    except Exception as e:
        logging.info(e)
        print e
        return ResponseBody(1, None)()
    finally:
        session.commit()
        session.close()


@app.route('/manage/editStudent/<sid>', methods=['POST'])
def editstudent(sid):
    session = DBSession()
    name = request.form['name']
    no = request.form['studentno']
    phone = request.form['phonenumber']
    email = request.form['studentemail']
    try:
        student = session.query(Student).filter(Student.id == sid).one()
        student.sname = name
        student.sno = no
        student.sphone = phone
        student.semail = email
        session.flush()
        return ResponseBody(0, None)()
    except Exception as e:
        logging.info(e)
        print e
        return ResponseBody(1, None)()
    finally:
        session.commit()
        session.close()


if __name__ == '__main__':
    app.run()
