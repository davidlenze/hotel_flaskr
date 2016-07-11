
    
# Hier alle erforderlichen Importe
import sqlite3
import os.path
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
 
# Festlegen der Konfiguration
DATABASE = '/skole/tjener/home0/lenzeda/Desktop/flaskr/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
 
# Instanziierung der Flask-Anwendung
app = Flask(__name__)
 
# Laden der Konfiguration ...
# ... durch Einlesen aller UPPERCASE Variablen durch die Funktion from_object()
app.config.from_object(__name__)
# ... oder durch Laden einer separaten config-Datei
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
 
# Kontakt zur Datebank herstellen


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        
@app.before_request
def before_request():
    g.db = connect_db()
 
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select id, text from entries order by id asc')
    entries = [dict(id=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (text) values (?)',
            [ request.form['text']])
    #g.db.execute('insert into entries (room) values (?)',
            #[ request.form['text']])
    #g.db.execute('insert into entries (customer) values (?)',
            #[ request.form['text']])
    #g.db.execute('insert into entries (recordno) values (?)',
            #[ request.form['integer']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            #return 'Hotelmanagnementsystem V1.0'
            #return redirect(url_for('show_entries'))
            #return redirect(url_for('show_entries'))
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


        
# Anwendung starten

if __name__ == '__main__':
   if not os.path.isfile('/skole/tjener/home0/lenzeda/Desktop/flaskr/flaskr.db'):
       
       init_db()
   app.run()
