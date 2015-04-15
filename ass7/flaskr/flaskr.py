#sqlite3 /tmp/flaskr.db < schema.sql

#Flask employee database main module
#Carlos Nikiforuk

# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# configuration
DATABASE = './flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application
app = Flask(__name__)
app.config.from_object(__name__)

# connect to db
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# initialize db if necessary
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# gets called before db request is made
@app.before_request
def before_request():
    g.db = connect_db()

# gets called after db request is done
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Admin login
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if not session.get('logged_in'):
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Invalid username'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for("show_options"))
        return render_template('login.html', error=error)
    else:
        return redirect(url_for('show_options'))

# options page with refs to forms
@app.route('/options')
def show_options():
    add = url_for('add_form')
    search = url_for('search_form')
    remove = url_for('remove_form')
    show = url_for('show_employees')
    return render_template('show_options.html', add=add, show=show, remove=remove, search=search)

# show employees
@app.route('/show')
def show_employees():
    cur = g.db.execute('select id, name, department from employees order by id asc')
    employees = [dict(id=row[0], name=row[1], department=row[2]) for row in cur.fetchall()]
    return render_template('show_employees.html', employees=employees)

# add employee form
@app.route('/add')
def add_form():
    if not session.get('logged_in'):
        abort(401)
    return render_template('add_employee.html')

# add employee post
@app.route('/add_employee', methods=['POST'])
def add_employee():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into employees (name, department) values (?, ?)',
                 [request.form['name'], request.form['department']])
    g.db.commit()
    flash('New entry was successfully added')
    return redirect(url_for('show_options'))

# remove employee form
@app.route('/remove')
def remove_form():
    if not session.get('logged_in'):
        abort(401)
    return render_template('remove_employee.html')

# remove employee post
@app.route('/remove_employee', methods=['POST'])
def remove_employee():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('delete from employees WHERE id=(?)', [request.form['id']])
    g.db.commit()
    flash('Entry was successfully removed')
    return redirect(url_for('show_options'))

# search employee form
@app.route('/search')
def search_form():
    if not session.get('logged_in'):
        abort(401)
    return render_template('search_employee.html')

# search employee post
@app.route('/search_employee', methods=['POST'])
def search_employee():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select id,name,department from employees where id=(?)', [request.form['id']])
    g.db.commit()
    employees = [dict(id=row[0], name=row[1], department=row[2]) for row in cur.fetchall()]
    return render_template('show_employees.html', employees=employees)

# admin logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
