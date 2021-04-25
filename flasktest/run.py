from flask import Flask
from flask import render_template
import random
app = Flask(__name__,
static_folder='./vuetest/dist/static',
template_folder = "./vuetest/dist")

@app.route('/')
def hello_world():
    return render_template('index.html',name='index')

@app.route('/mytest')

def test(): 
    name = 'chenxin'
    return {
        'name': name,
        'randnum1': str(random.randint(1,100)),
        'randnum2': str(random.randint(101,500))    
    }

def test111(): 
    randnum = dict()
    randnum['randnum1'] = str(random.randint(500,1000))
    return randnum

if __name__ == '__main__':
    app.run()