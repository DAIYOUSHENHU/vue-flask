from sqlite3.dbapi2 import SQLITE_INSERT
from types import MethodType
from flask import Flask, request, jsonify
from flask import render_template
import sqlite3
from flask import g
import random

app = Flask(__name__,
            static_folder='./vuetest/dist/static',
            template_folder="./vuetest/dist")

DATABASE = './path/to/database.db'
# 创建表格、插入数据
# @app.before_first_request
# def create_db():
#   # 连接
#   conn = sqlite3.connect(DATABASE)
#   c = conn.cursor()
#   # 创建表
#   c.execute('''DROP TABLE IF EXISTS user''')
#   c.execute('''DROP TABLE IF EXISTS chessmap''')
#   c.execute('''CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
#   c.execute('''CREATE TABLE chessmap (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,  mapx TEXT, mapy TEXT, color TEXT, step INTEGER)''')
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
# # 关闭
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


def op_db(insert, args=()):
    db = get_db()
    db.execute(insert, args)
    db.commit()
    db.close()


@app.route('/')
def hello_world():
    return render_template('index.html', name='index')

    # 用户登录


@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    dbpass = query_db(
        "SELECT password FROM user WHERE username = ?", args=(username,))
    if password == dbpass[0][0]:
        return {
            'msg': 'success',
        }
    else:
        return {
            'msg': 'false'
        }

# 用户注册


@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    dbres = query_db("SELECT * FROM user WHERE username = ?", args=(username,))
    if dbres:
        return {
            'msg': 'exist'
        }
    else:
        op_db("INSERT INTO user(username, password) VALUES (?,?)",
              (username, password))
        return {
            'msg': 'success',
        }


@app.route("/chessing", methods=['POST'])
def chessing():
    username = request.form['username']
    mapx = request.form['mapx']
    mapy = request.form['mapy']
    color = request.form['color']
    step = int(request.form['step'])
    op_db("INSERT INTO chessmap(username, mapx, mapy, color, step) VALUES (?,?,?,?,?)",
          (username, mapx, mapy, color, step))

    # checkwin
    winner = ''
    res = []
    for i in range(15):
        res.append([0] * 15)
    mode = []
    mode.append([0, 1]),
    mode.append([1, 0]),
    mode.append([1, 1]),
    mode.append([1, -1]),
    resdb = query_db("SELECT * FROM chessmap WHERE username = ?", (username,))
    for item in resdb:
        res[int(item[2])][int(item[3])] = int(item[4])

    # checkwin(mapx, mapy, color, mode)
    for k in range(4):
        count = 1
        for i in range(1, 5):
            if int(mapx) + i * mode[k][0] <= 14 and int(mapy) + i * mode[k][1] <= 14:
                if res[int(mapx) + i * mode[k][0]][int(mapy) + i * mode[k][1]] == int(color):
                    count += 1
                else:
                    break

        for i in range(1, 5):
            if int(mapx) - i * mode[k][0] <= 14 and  int(mapy) - i * mode[k][1] <= 14:
                if res[int(mapx) - i * mode[k][0]][int(mapy) - i * mode[k][1]] == int(color):
                    count += 1
                else:
                    break
         
        if (count >= 5):
          winner = int(color)

    return {
        'msg': winner
    }

    # return {
    #   'username': username,
    #   'mapx': mapx,
    #   'mapy': mapy,
    #   'color': color,
    #   'msg': 'success',
    # }

    # 获取原数据


@app.route("/getmap", methods=['POST'])
def getmap():
    username = request.form['username']
    resdb = query_db("SELECT * FROM chessmap WHERE username = ?", (username,))
    res = []
    for item in resdb:
        res.append([item[2], item[3], item[4], item[5]])

    return {
        'res': res
    }

# 悔棋


@app.route("/regret", methods=['POST'])
def regret():
    username = request.form['username']
    step = request.form['step']
    op_db("DELETE FROM chessmap WHERE username = ? AND step = ?", (username, step,))
    return {
        'msg': 'regret'
    }

# 重新开始


@app.route("/newgame", methods=['POST'])
def newgame():
    username = request.form['username']
    op_db("DELETE FROM chessmap WHERE username = ?", (username,))
    return {
        'msg': 'newgame'
    }


if __name__ == '__main__':
    app.run()
