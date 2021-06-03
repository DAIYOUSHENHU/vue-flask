from sqlite3.dbapi2 import SQLITE_INSERT
from types import MethodType
from flask import Flask, request, jsonify
from flask import render_template
import sqlite3
from flask import g
import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16

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

@app.route("/speak")
def speak():
    flag = False
    num = []
    change =  {
        '零': '0',
        '一': '1',
        '二': '2',
        '三': '3',
        '四': '4',
        '五': '5',
        '六': '6',
        '七': '7',
        '八': '8',
        '九': '9',
        '十': '10',
    }
    devpid = 1536
    my_record()
    TOKEN = getToken(HOST)
    speech = get_audio(FILEPATH)
    result = speech2text(speech, TOKEN, devpid)
    res = ''
    for i in result:
        if i == "第":
            flag = True
            continue
        if i == '行' or i == '列':
            flag = False
            if len(res) > 2:
                res = res[0] + res[-1] 
            num.append(res)
            res = ''  
        if flag:
            res += change[i]           
    if num[0] and num[1] and int(num[0])<=15 and int(num[1])<=15:
        return {
            'msg': num
        }
    else:
        return{
            'msg': 'faild'
        }    

framerate = 16000  # 采样率
num_samples = 2000  # 采样点
channels = 1  # 声道
sampwidth = 2  # 采样宽度2bytes
FILEPATH = 'speech.wav'

base_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
APIKey = "L77rFuX5Mv1GNxK8XQFnz7gA"
SecretKey = "eBLb3u9RVNG4EYvjIDqXrLGDQ1B8VTKh"

HOST = base_url % (APIKey, SecretKey)


def getToken(host):
    res = requests.post(host)
    return res.json()['access_token']


def save_wave_file(filepath, data):
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b''.join(data))
    wf.close()


def my_record():
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=channels,
                     rate=framerate, input=True, frames_per_buffer=num_samples)
    my_buf = []
    # 录音
    t = time.time()

    while time.time() < t + 4:  # 秒
        string_audio_data = stream.read(num_samples)
        my_buf.append(string_audio_data)

    save_wave_file(FILEPATH, my_buf)
    stream.close()


def get_audio(file):
    with open(file, 'rb') as f:
        data = f.read()
    return data


def speech2text(speech_data, token, dev_pid=1537):
    FORMAT = 'wav'
    RATE = '16000'
    CHANNEL = 1
    CUID = '*******'
    SPEECH = base64.b64encode(speech_data).decode('utf-8')

    data = {
        'format': FORMAT,
        'rate': RATE,
        'channel': CHANNEL,
        'cuid': CUID,
        'len': len(speech_data),
        'speech': SPEECH,
        'token': token,
        'dev_pid': dev_pid
    }
    url = 'https://vop.baidu.com/server_api'
    headers = {'Content-Type': 'application/json'}
    
    # 识别  
    r = requests.post(url, json=data, headers=headers)
    Result = r.json()
    if 'result' in Result:
        return Result['result'][0]
    else:
        return Result


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
