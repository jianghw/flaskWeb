import sqlite3
from contextlib import closing

from flask import Flask, g

app = Flask(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """
    初始化数据库
    :return:
    """
    with closing(connect_db()) as db:
        with app.open_resource('app/db.sql') as f:
            sql = f.read().decode()
            db.cursor().executescript(sql)
        db.commit()


@app.before_request
def before_request():
    """
    在 Flask 提供的 g 特殊对象中
    这个对象只能保存一次请求的信息， 并且在每个函数里都可用
    :return:
    """
    g.db = connect_db()


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [
        dict((cur.description[idx](0), value) for idx, value in enumerate(row))
        for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else None


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


if __name__ == '__main__':
    app.debug = True
    app.config.from_object('app.blog')

    init_db()
    app.run(host='127.0.0.1', port='5000')
