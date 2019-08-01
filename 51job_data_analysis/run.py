"""
    Create by GL on 2019-08-01
"""
from flask import Flask, render_template

from ArticleSpider.models.base import db

app = Flask(__name__)
app.config.from_object('')
db


@app.route('/')
def index():
    return 'Hello World'


@app.route('/51job')
def a51job():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
