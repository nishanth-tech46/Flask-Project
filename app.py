
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT,
                  course TEXT 
              )""")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        return f"""
        <h1> Message Sent Successfully! </h1>
        <p>Name: {name}</p>
        <p>Email: {email}</p>
        <p>Message: {message}</p>
        """
    return render_template('contact.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, course) VALUES (?, ?, ?)", (name, email, course))

        conn.commit()
        conn.close()
        print("Users table created successfully")
        return redirect('/students')
    return render_template('register.html')

@app.route('/students')
def students():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    students = cur.fetchall()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/test')
def test():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()

    conn.close()
    return str(tables)

if __name__ == '__main__':
    create_table()
    print("Users table created successfully")
    app.run(debug=True)