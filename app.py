from flask import Flask, render_template, json, request, redirect
import sqlite3
app = Flask(__name__)

global lst
global name
name = ''
lst = ['1', ' ', '3']
global sm
sm = 0

global dd
dd = {}




@app.route('/', methods=['GET'])
def index():
    con = sqlite3.connect('flask_user_data.db')

    cur = con.cursor()
    print(cur.execute('''SELECT * FROM data''').fetchall())
    if request.remote_addr not in cur.execute('''SELECT * FROM data''').fetchall():
        try:

            cur.execute("INSERT INTO data VALUES (?, ?, ?)", ('', request.remote_addr, '0'))
        except sqlite3.IntegrityError:
            pass
    print(request.remote_addr, '1')
    a = cur.execute('''SELECT * from data WHERE ip = ?''', (str(request.remote_addr), )).fetchall()[0]
    b = cur.execute('''SELECT * from data''').fetchall()
    con.commit()
    con.close()
    return render_template('index.html', lst=a[2], sorter_lst=b, len=len(b))


@app.route('/', methods=['POST'])
def get_len_1():
    global dd
    global sm
    con = sqlite3.connect('flask_user_data.db')

    cur = con.cursor()
    print(request, '2')
    edit, click = request.form.get('edit'), request.form.get('click')
    if edit is not None:
        con.commit()
        con.close()
        return redirect('/edit/')
    else:
        n = cur.execute('''SELECT * from data WHERE ip = ?''', (str(request.remote_addr), )).fetchall()[0][2]
        n += 1
        cur.execute('''UPDATE data
        SET counter = ?
        WHERE ip = ?''', (str(n), request.remote_addr))
        con.commit()
        con.close()
        return redirect('/')

@app.route('/edit/')
def edit():
    return render_template('edit.html')

@app.route('/edit/', methods=['POST'])
def edit_post():
    con = sqlite3.connect('flask_user_data.db')

    cur = con.cursor()
    edit, click = request.form.get('edit'), request.form.get('click')
    if click is not None:
        con.commit()
        con.close()
        return redirect('/')
    else:

        name = request.form.get('name')
        cur.execute('''UPDATE data
                SET name = ?
                WHERE ip = ?''', (name, request.remote_addr))
        con.commit()
        con.close()
        return redirect('/edit/')
if __name__ == "__main__":
    app.run(host='192.168.1.72')

