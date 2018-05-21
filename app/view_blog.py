from flask import render_template, g, request, session, flash, redirect, url_for, abort

from app.run_blog import app, query_db


@app.route('/')
@app.route('/index/')
@app.route('/index/<int:page>')
def index(page=1):
    if not session['ses_login']:
        return redirect(url_for('login'))
    return redirect(url_for('login_success'))


@app.route('/')
def login_success():
    rows = query_db('select * from blog ')
    if not rows:
        return render_template('show_table.html', rows=rows)
    return render_template('inset_table.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['user_name'] != app.config['USERNAME']:
            error = 'invalid your name'
        elif request.form['user_psd'] != app.config['PASSWORD']:
            error = 'invalid your password'
        else:
            session['ses_login'] = True
            flash('you login success')
            return redirect(url_for('index'))
        return render_template('login.html', error=error)
