# -*- coding: utf-8 -*-
import MySQLdb as mysql
import logging
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response, json
from models import DBSession, Admin, Student
from responsebody import ResponseBody
from page import Page


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
        return redirect(url_for('showstudents', pageindex=1))


@app.route('/signout')
def signout():
    try:
        resp = make_response(redirect(url_for('login')))
        resp.delete_cookie('username')
        return resp
    except Exception as e:
        print e


@app.route('/auth', methods=['POST'])
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
            resp = make_response(redirect(url_for('showstudents', pageindex=1)))
            resp.set_cookie('username', username)
            return resp
    except Exception as e:
        logging.info(e)
        print e
        return ResponseBody(1, None)()
    finally:
        session.close()


@app.route('/showStudents/<pageindex>')
def showstudents(pageindex):
    username = request.cookies.get('username')
    if username is None:
        return redirect(url_for('login'))
    session = DBSession()
    student_count = session.query(Student).count()
    page_size = 5
    page = Page(student_count, int(pageindex), page_size)
    try:
        students = session.query(Student).offset(page.offset).limit(page.limit)
        list = []
        for i in students:
            list.append(i.to_dict())
        # list.append(page.__dict__)
        # return ResponseBody(0, list).getContent()
        return render_template("showStudent.html", list=list, page=page.__dict__)
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
    address = request.form['address']
    try:
        student = Student(name, no, phone, email, address)
        session.add(student)
        return ResponseBody(0, None)()
        # return redirect(url_for('showstudents', pageindex=1))
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
    address = request.form['address']
    try:
        student = session.query(Student).filter(Student.id == sid).one()
        student.sname = name
        student.sno = no
        student.sphone = phone
        student.semail = email
        student.param1 = address
        session.flush()
        return ResponseBody(0, None)()
    except Exception as e:
        logging.info(e)
        print e
        return ResponseBody(1, None)()
    finally:
        session.commit()
        session.close()


@app.route('/search', methods=['POST'])
def searchstudent():
    session = DBSession()
    index = request.form['search']
    try:
        if '0' <= index[0] <= '9':
            try:
                student = session.query(Student).filter(Student.sno == index)
                list = []
                for i in student:
                    list.append(i.to_dict())
                if list == []:
                    return ResponseBody(0, None)()
                else:
                    return ResponseBody(0, list)()
            except Exception as e:
                print e
                return ResponseBody(0, None)()
        else:
            try:
                student = session.query(Student).filter(Student.sname == index)
                list = []
                for i in student:
                    list.append(i.to_dict())
                if list == []:
                    return ResponseBody(0, None)()
                else:
                    return ResponseBody(0, list)()
            except Exception as e:
                print e
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
