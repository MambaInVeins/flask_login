from flask import Flask,render_template, request, session, redirect, url_for, jsonify
import hashlib
import pymysql


from settings import MYSQL_DB_NAME,MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD
account = Flask('account')
account.config['SECRET_KEY'] = 'hard to guess string'

@account.route('/', methods=["GET", "POST"])
@account.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        if (user == "" or pwd == ""):
            return jsonify({"code": 401, "error": "账号和密码不可为空!"})
        querycmd = "SELECT * FROM user WHERE username='%s'" % (user)
        conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB_NAME, charset='utf8')
        cursor = conn.cursor()
        cursor.execute(querycmd)
        certificate = cursor.fetchone()

        hl = hashlib.md5()
        hl.update(pwd.encode(encoding='utf-8'))
        if (certificate==None):
            return jsonify({"code": 401, "error": "该账号不存在!"})
        else:
            if (user == certificate[0] and hl.hexdigest() == certificate[1]):
                session['user'] = user
                return jsonify({"code": 200, "error": ""})
            else:
                return jsonify({"code": 401, "error": "用户名或密码错误"})


@account.route('/logout')
def logout():
    del session['user']
    return redirect(url_for('login'))

@account.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port='5000',debug=True)
    account.run(host='127.0.0.1',port='5002',debug=True,threaded=True)