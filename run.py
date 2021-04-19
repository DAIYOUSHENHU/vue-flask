from flask import Flask
from flask import render_template
app = Flask(__name__,
static_folder='./vuetest/dist/static',
template_folder = "./vuetest/dist")

@app.route('/')
def hello_world():
    return render_template('index.html',name='index')

if __name__ == '__main__':
    app.run()