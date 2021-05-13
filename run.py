from sqlite3.dbapi2 import SQLITE_INSERT
from types import MethodType
from flask import Flask, request, jsonify
from flask import render_template
import sqlite3
from flask import g
import random

app = Flask(__name__,
static_folder='./vuetest/dist/static',
template_folder = "./vuetest/dist")

DATABASE = './path/to/database.db'
# 创建表格、插入数据
# @app.before_first_request
# def create_db():
#   # 连接
#   conn = sqlite3.connect(DATABASE)
#   c = conn.cursor()
#   # 创建表
  # c.execute('''DROP TABLE IF EXISTS user''')
  # c.execute('''DROP TABLE IF EXISTS chessmap''')
  # c.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
  # c.execute('''CREATE TABLE chessmap (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,  mapx TEXT, mapy TEXT, color TEXT)''')
  # 数据
  # 格式：用户名,邮箱
  # purchases = [('admin', 'admin'),
  #        ('111', '123456'),
  #        ('guest2', '123456'),
  #        ('guest3', '123456'),
  #        ('guest4', '33456')]
  # # 插入数据
  # c.executemany('INSERT INTO user(username, password) VALUES (?,?)', purchases)

  # conn.commit()
  # 关闭
  # conn.close()

def get_db():
  db = sqlite3.connect(DATABASE)
  db.row_factory = sqlite3.Row
  return db

def query_db(query, args=(), one=False):
  db = get_db()
  cur = db.execute(query, args)
  db.commit()
  rv = cur.fetchall()
  db.close()
  return (rv[0] if rv else None) if one else rv

def insert_db(insert, args=()):
  db = get_db()
  db.execute(insert, args)
  db.commit()
  db.close()

@app.route('/')
def hello_world():
    return render_template('index.html',name='index')

@app.route("/mytest/alluser")
def users():
  res = query_db("SELECT * FROM user WHERE id <= ?", args=(10,))
  return "<br>".join(["{0}: {1}: {2}".format(user[1], user[2], user[0]) for user in res])

@app.route("/mytest/user/<username>")
def user(username):
  res = query_db("SELECT * FROM user WHERE id = ?", args=(username,)) #不妨设定：第一次只返回6个数据
  return {
    'id': res[0][0],
    'name': res[0][1],
    'email': res[0][2]
  } 
@app.route("/login", methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  dbpass = query_db("SELECT password FROM user WHERE username = ?",args=(username,))
  if password == dbpass[0][0]:  
    return {
    'msg': 'success',
    }
  else :
    return {
      'msg': 'false'
    }

@app.route("/register", methods=['POST'])
def register():
  username = request.form['username']
  password = request.form['password']
  dbres = query_db("SELECT * FROM user WHERE username = ?",args=(username,))
  if dbres:
    return {
      'msg': 'exist'
    }
  else:
    insert_db("INSERT INTO user(username, password) VALUES (?,?)",(username, password))
    return {
      'msg': 'success',
    }
  
@app.route("/chessing", methods=['POST'])
def chessing():
  username = request.form['username']
  mapx = request.form['mapx']
  mapy = request.form['mapy']
  color = request.form['color']
  insert_db("INSERT INTO chessmap(username, mapx, mapy, color) VALUES (?,?,?,?)",(username, mapx, mapy, color))
  return {
    'username': username,
    'mapx': mapx,
    'mapy': mapy,
    'color': color,
    'msg': 'success',
  }
  
@app.route("/getmap", methods=['POST'])
def getmap():
  username = request.form['username']
  res = query_db("SELECT * FROM chessmap WHERE username = ?",(username,))
  return "<br>".join(["{0}: {1}: {2}".format(user[2], user[3], user[4]) for user in res])

  # return {
  #   'res': res,
  #   'msg': 'success'
  # }  

@app.route('/mytest')
def test(): 
    name = 'chenxin'
    return {
        'name': name,
        'randnum1': str(random.randint(1,100)),
        'randnum2': str(random.randint(101,500))    
    }


if __name__ == '__main__':
    app.run()