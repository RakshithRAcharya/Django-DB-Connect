from sqlite3 import DatabaseError, InternalError
from django.db import OperationalError, ProgrammingError
from django.shortcuts import render, redirect
from .models import DB
from .forms import DBForm
from django.contrib import messages

import pymysql
import psycopg2
import cx_Oracle

form_data = globals()

def home(request):
    return render(request, 'main_page.html', {})

def get_DB_details(request):
    db_server=''
    db_host=''
    db_name=''
    db_port=''
    db_login_username=''
    db_login_password=''

    context ={}
    form = DBForm(request.POST or None, request.FILES or None, initial=request.session.get('form_data'))
    
    context = {'form': form,'db_server':db_server, 'db_host':db_host, 'db_name':db_name, 'db_port':db_port, 'db_login_username':db_login_username, 'db_login_password':db_login_password}
    return render(request, 'db_details.html', context)


def login(request):
    db_server = request.POST.get('db_server')
    db_host = request.POST.get('db_host')
    db_name = request.POST.get('db_name')
    db_port = int(request.POST.get('db_port'))
    db_login_username = request.POST.get('db_login_username')
    db_login_password = request.POST.get('db_login_password')
    db_details = {'db_server':db_server, 'db_host':db_host, 'db_name':db_name, 'db_port':db_port, 'db_login_username':db_login_username, 'db_login_password':db_login_password}

    form = DBForm( request.POST or None, request.FILES or None, initial=request.session.get('form_data'))

    if db_server == 'MYSQL' or db_server == 'mysql':
        try:
            conn = pymysql.connect(host= db_host, port=db_port, user=db_login_username, passwd=db_login_password)
        except (ConnectionError, pymysql.OperationalError, pymysql.ProgrammingError, pymysql.InternalError, DatabaseError) as e :
            messages.error(request, ('DB Details entered are wrong'))
            return redirect('getDB')
    elif db_server == 'POSTGRE' or db_server == 'postgresql' or db_server == 'POSTGRESQL':
        try:
            conn = psycopg2.connect( host=db_host, user=db_login_username, password=db_login_password, dbname=db_name )
        except (ConnectionError, OperationalError, ProgrammingError, InternalError, DatabaseError):
            messages.error(request, ('DB Details entered are wrong'))
            return redirect('connect')
    elif db_server == 'ORACLE' or db_server == 'ORACLEDB' or db_server == 'oracle':
        try:
            conn = cx_Oracle.connect(host=db_host, user=db_login_username, password=db_login_password, dbname=db_name)
        except (ConnectionError, OperationalError, ProgrammingError, InternalError, DatabaseError):
            messages.error(request, ('DB Details entered are wrong'))
            return redirect('connect')

    if form.is_valid() and conn:
        form.save()
        messages.success(request, ("You successfully logged in"))
    else:
        return redirect('connect')

    data = []
    if db_server == 'MYSQL' or db_server == 'mysql':
        try:
            con = pymysql.connect(host= db_host, port=db_port, user=db_login_username, passwd=db_login_password)
            cur = con.cursor()
            cur.execute('USE {0}'.format(db_name))
            cur.execute('SHOW TABLES')
            for (table_name,) in cur:
                data.append(table_name)
        except pymysql.DatabaseError as err:
            print(err)
        finally:
            if con:
                cur.close()
                con.close()
    
    elif db_server == 'POSTGRE' or db_server == 'postgresql' or db_server == 'POSTGRESQL':
        try:
            con = psycopg2.connect( host=db_host, user=db_login_username, password=db_login_password, dbname=db_name )
            cur = con.cursor()
            cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
            q = cur.fetchall()
            for i in q:
                data.append(i)
        except pyscopg2.DatabaseError as err:
            print(err)
        finally:
            if con:
                cur.close()
                con.close()

    elif db_server == 'ORACLE' or db_server == 'ORACLEDB' or db_server == 'oracle':
        try:
            con = cx_Oracle.connect(host=db_host, user=db_login_username, password=db_login_password, dbname=db_name)#1512
            cur = con.cursor()
            cur.execute('SELECT table_name  FROM dba_tables')
            for row in cur:
                data.append(row)
        except cx_Oracle.Error as error:
            print(error)
        finally:
            if con:
                cur.close()
                con.close()


    form_data['form'] = db_details
    return render(request, 'tables.html', {'data':data})

def show(request):
    table_name = request.POST.get('show')
    data = form_data['form']
    db_server = data['db_server']
    db_host = data['db_host']
    db_name = data['db_name']
    db_port = data['db_port']
    db_login_username = data['db_login_username']
    db_login_password = data['db_login_password']

    data = []

    if db_server == 'MYSQL' or db_server == 'mysql':
        con = pymysql.connect(host= db_host, port=db_port, user= db_login_username, passwd=db_login_password)
        cur = con.cursor()
        cur.execute('USE {0}'.format(db_name))
        cur.execute('SELECT * from {0} LIMIT 10'.format(table_name))
        for rows in cur:
            data.append(rows)
    
    elif db_server == 'POSTGRE' or db_server == 'postgresql' or db_server == 'POSTGRESQL':
        con = psycopg2.connect( host=db_host, user=db_login_username, password=db_login_password, dbname=db_name )
        cur = con.cursor()
        data = cur.execute('SELECT table_name FROM information_schema.tables ORDER BY table_name;')

    elif db_server == 'ORACLE' or db_server == 'ORACLEDB' or db_server == 'oracle':
        con = cx_Oracle.connect(host=db_host, user=db_login_username, password=db_login_password, dbname=db_name)#1512
        cur = con.cursor()
        data = cur.execute('')

    return render(request, 'table_data.html', {'data':data})


def app_data(request):
    app_data = DB.objects.all()
    return render(request, 'app_db.html', {'app_data': app_data})