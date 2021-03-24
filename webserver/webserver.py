import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('Kaffee.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user(user_id):
    conn = get_db_connection()
    post = conn.execute('SELECT coffees FROM kaffeeliste WHERE hash = ?', (user_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)

@app.route('/registration', methods =('GET','POST'))
def index():
    if request.method == 'POST':
        name = request.form['name']
        mhash = request.form['hash']

        if not mhash or not name:
            flash("Bitte Zeichenfolge und Namen eintragen")
        else:
            conn = get_db_connection()
            sql = '''UPDATE KAFFEELISTE\
            SET NAME = ?\
            WHERE HASH = ? ;'''
            conn.execute(sql,(name,mhash))
            conn.commit()
            conn.close()
            return redirect(url_for('user',user_id=mhash))
    return render_template('reg_form.html')

@app.route('/<int:user_id>')
def user(user_id):
    user = get_user(user_id)
    return render_template('user.html', user=user)

@app.route('/admin_listview')
def admin_listview():
    connn = get_db_connection()
    users = conn.execute('SELECT name, coffees, paid FROM kaffeeliste').fetchall()
    conn.close()
    return render_template('admin_listview.html', users = users)
