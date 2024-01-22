from flask import jsonify,Flask, render_template,abort, request, url_for, redirect
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename
import os


# Flask 애플리케이션 생성
app = Flask(__name__, template_folder='templates')

# mysql 연동 (project_a에 테이블 생성 필요)
conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="1234", database="project_a")
cursor = conn.cursor()

# 메인페이지
@app.route('/')
def index():
    return render_template('index.html')


# 미세먼지 예측 데이터
@app.route('/polygon')
def city():
    return render_template('polygon.html')

# 로그인
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']# form 태그의 name 이 email의 value 값을 가져온다.
    password_candidate = request.form['password1']
    print(email, password_candidate)

    cur = conn.cursor()
    # mysql의 email 값을 사용하여 해당되는 데이터 값을 가져와서 변수에 저장
    result = cur.execute("SELECT * FROM register_tbl WHERE email = %s", [email])
    print('result', result)
    if result > 0:

        data = cur.fetchone()# fetchone을 사용하여 첫 번째 행 가져오기
        print(data)
        password_db = data[4]
        print('password', password_db)
        # DB저장 된 데이터와 사용자가 입력한 데이터의 조건이 성립하면 index.html로 넘어간다
        if (password_candidate == password_db):
            return render_template("result.html")

        else:
            return render_template('login.html')


# 회원가입
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def register_input():
    email = request.form['email']
    name = request.form['name']
    password1 = request.form['password1']
    password2 = request.form['password2']
    gender = request.form['gender']
    if password1 != password2:  # 비밀번호 확인
        return "비밀번호가 일치하지 않습니다."
    try:
        cursor.execute("""
               INSERT INTO register_tbl (email, name, password1,password2, gender)
               VALUES (%s, %s, %s, %s,%s)
                """, (email, name, password1,password2, gender))
        conn.commit()
        return render_template('register.html', success=True)
    except Exception as e:
        conn.rollback()
        return render_template('register.html', error="이미 등록된 계정입니다.")


# 리액트 서버
@app.route('/start_react_server', methods=['GET'])
def start_react_server():
    try:
        subprocess.Popen('cd /d C:\\react-news && npm start', shell=True)
        return jsonify({'message': 'React server started successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

# 뉴스
@app.route('/react-news/test/src/<path:filename>')
def react_news(filename):
    return send_from_directory('C:/react-news/test/src', filename)


if __name__ == '__main__':
    app.run(debug=True)

