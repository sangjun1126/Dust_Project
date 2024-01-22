from flask import jsonify,Flask, render_template,abort, request, url_for, redirect
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename
import os
app = Flask(__name__, template_folder='templates')

conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="1234", database="project_traning")
cursor = conn.cursor()

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']# form 태그의 name 이 email의 value 값을 가져온다.
    password_candidate = request.form['password1']
    print(email, password_candidate)

    cur = conn.cursor()
    result = cur.execute("SELECT * FROM register_tbl WHERE email = %s", [email])# mysql의 email 값을 사용하여 해당되는 데이터 값을 가져와서 변수에저장
    print('result', result)
    if result > 0:

        data = cur.fetchone()# fetchone을 사용하여 첫 번째 행 가져오기
        print(data)
        password_db = data[4]
        print('password', password_db)
        if (password_candidate == password_db):# DB저장 된 데이터와 사용자가 입력한 데이터의 조건이 성립하면 index.html로 넘어간다
            return render_template("result.html")

        else:
            return render_template('login.html')
@app.route('/memberlist')
def memberlist():
    cursor.execute("SELECT * FROM register_tbl")
    data = cursor.fetchall()
    dict={"uno":[],"email":[], "name":[], "password1":[], "password2":[], "gender":[]}
    for i in data:
        for idx, k in enumerate(dict.keys()):
            dict[k].append(i[idx])
    print(dict)
    return render_template('memberlist.html',data= dict)

@app.route('/view')
def memberlist_num():
    a = request.args.get("a")
    print(a)
    cursor.execute("SELECT * FROM register_tbl where uno=%s",(a,))
    data = cursor.fetchall()
    data_column = data[0]
    print(data_column)
    return render_template('view_1.html', data=data)

@app.route('/update_data', methods=['POST'])
def update_data():

    uno_value = request.form.get()
    email_value = request.form.get()


    a_value = request.args.get("a")


    cursor.execute("UPDATE register_tbl SET uno_value = %s, email_value = %s WHERE uno = %s",
                   (uno_value, email_value, a_value))


    conn.commit()

    render_template('memberlist.html')

@app.route('/update_member', methods=['POST'])
def update():
    uno_value = request.form['uno']
    email_value = request.form['email']
    name_value = request.form['name']
    password1_value = request.form['password1']
    password2_value = request.form['password2']
    gender_value = request.form['gender']
    print(uno_value, email_value, name_value, password1_value , password2_value, gender_value)

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE register_tbl SET email = %s, name = %s, password1 = %s, password2 = %s, gender = %s WHERE uno = %s",
            (email_value, name_value, password1_value, password2_value, gender_value,uno_value))
        print("여기 들어오는가?")
        conn.commit()
    updated_data = cursor.execute

    return render_template('view.html', data=updated_data)

def get_updated_data_somehow(uno):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM register_tbl WHERE uno = %s", (uno,))
        updated_data = cursor.fetchall()
    return updated_data

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


@app.route("/board_view", methods=["GET", "POST"])
def board_view():
    return render_template("board_write.html")

@app.route("/board_test")
def board_test():
    return render_template("board_test.html")

if not os.path.exists("uploads"): #(uploas)  디렉토리 존재여부 확인
    os.makedirs("uploads") # 디렉토리가존재 하지않으면 (uploads) 디렉토리를 생성


@app.route('/ajax_comment', methods=['POST'])
def ajax_comment():
    print("들어와라 얍 ")
    try:
        data = request.json   # POST 요청으로 부터 JSON 데이터를 추출합니다.
        comment_value = data['comment']
        post_num = data['post_num']
        # 위의 코드 2줄은 JSON 데이터에서 해당 필드 값을 가져오는 코드

        sql_insert_1 = 'INSERT INTO comments (post_num, comment_text) VALUES (%s, %s)'
        cursor.execute(sql_insert_1, (post_num, comment_value))
        conn.commit() # 데이터베이스에 대한 변경 사항을 확정하는 코드
        print("여기는 문제가 없는가? ")
        sql_insert_list = "SELECT * FROM comments WHERE post_num = %s"
        cursor.execute(sql_insert_list, (post_num,))
        comment_list = cursor.fetchall() # 댓글 목록을 가져 옵니다.
        # coments 테이블에서 post_num 해당 하는 값
        print("여기도 문제 없니?")
        print(comment_list,"여기 들어옴?")
        return jsonify({'comment': comment_list,'post_num':post_num})

        # 글 목록과 게시물 번호를 JSON 형식으로 반환합니다.
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'Invalid JSON data'}),

@app.route('/ajax_comment/update', methods=['POST'])
def update_comment():
    try:
        data = request.json
        post_num = data['post_num']
        old_comment_text = data['comment_id']  # 필드 이름 수정
        new_comment_text = data['new_comment_text']

        sql_update_comment = 'UPDATE comments SET comment_text = %s WHERE post_num = %s AND comment_text = %s'
        cursor.execute(sql_update_comment, (new_comment_text, post_num, old_comment_text))
        conn.commit()

        sql_select_comments = "SELECT * FROM comments WHERE post_num = %s"
        cursor.execute(sql_select_comments, (post_num,))
        comment_list = cursor.fetchall()

        return jsonify({'comment': comment_list, 'post_num': post_num})
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/ajax_comment/delete', methods=['POST'])
def delete_comment():
    print("여기는 들어오는가 삭제 댓글")
    try:
        data = request.json
        post_num = data['post_num']
        comment_id = data['comment_id']  # 필드 이름 수정
        print('post_num:', post_num,'comment_id:' , comment_id)
        sql_delete_comment = 'DELETE FROM comments WHERE post_num = %s AND id = %s'  # 필드 이름 수정
        cursor.execute(sql_delete_comment, (post_num, comment_id))
        conn.commit()

        sql_select_comments = "SELECT * FROM comments WHERE post_num = %s"
        cursor.execute(sql_select_comments, (post_num,))
        comment_list = cursor.fetchall()

        return jsonify({'comment': comment_list, 'post_num': post_num})
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500


@app.route("/board_write", methods=["GET", "POST"])
def write_post():
    if request.method == "POST":
        title = request.form['title']
        writer = request.form['writer']
        password = request.form['password']
        content = request.form['content']
        image_path = None  # 기본값으로 None 설정

        if 'image' in request.files: # image 파일이 있는지 확인
            image = request.files['image']
            if image.filename != '': # 이미지파일의 이름이 비어 있지 않는지 확인
                filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + secure_filename(image.filename)#현재 날짜와 시간을 이용하여 고유한 파일 이름 생성
                image.save(os.path.join("uploads", filename)) #
                image_path = "uploads/" + filename

        sql_insert_1 = 'INSERT INTO board_tbl (title, writer, password, content, image_path) VALUES (%s, %s, %s, %s, %s)'
        try:
            cursor.execute(sql_insert_1, (title, writer, password, content, image_path))
            conn.commit()
            print("데이터베이스에 성공적으로 저장되었습니다.")
        except Exception as e:
            print(f"데이터베이스 저장 중 오류 발생: {e}")
            conn.rollback()

    return redirect(url_for('board_list'))

@app.route("/board_list")
def board_list():
    per_page = 10
    page = request.args.get('page', 1, type=int)

    total_cnt_query = "SELECT count(*) FROM board_tbl"
    cursor.execute(total_cnt_query)
    total_cnt = cursor.fetchone()[0]

    total_pages = (total_cnt + per_page - 1) // per_page

    offset = (page - 1) * per_page


    sql = "SELECT * FROM board_tbl LIMIT %s OFFSET %s"
    cursor.execute(sql, (per_page, offset))
    data_list = cursor.fetchall()

    dict_mapping = {
        '0': 'num',
        '1': 'title',
        '2': 'writer',
        '3': 'password',
        '4': 'date',
        '5': 'image_path',
        '6': 'content'
    }
    dict_result = {key: [] for key in dict_mapping.values()}

    for row in data_list:
        for idx, data in enumerate(row):
            key = dict_mapping[str(idx)]
            dict_result[key].append(data)

    data_to_display = {
        'data_list': dict_result,
        'total_pages': total_pages,
        'page': page
    }
    return render_template("board_list.html", **data_to_display)

@app.route('/detail/<int:num>')
def detail(num):
    # 'num'에 대한 세부 정보를 가져오기 위한 로직을 여기에 추가
    print(num)
    per_page = 10  # 페이지당 아이템 수
    page = 1  # 기본 페이지

    # 페이지 파라미터가 전달되었다면 해당 페이지로 설정
    if 'page' in request.args:
        page = int(request.args['page'])

    # 올바른 페이지 계산을 위해 OFFSET 값을 계산
    offset = (page - 1) * per_page

    sql = "SELECT * FROM board_tbl WHERE num=%s LIMIT %s OFFSET %s"
    cursor.execute(sql, (num, per_page, offset))
    data = cursor.fetchall()
    if not data:
        abort(404)
    # 댓글 정보 가져오기 (삭제한 코드 블록을 여기에 추가)
    # sql = "SELECT * FROM comments WHERE post_num=%s"
    # cursor.execute(sql, (num,))
    # comments_data = cursor.fetchall()
    dict_result = {}
    for idx, d in enumerate(data[0]):
        dict_result[idx] = d

    print(dict_result)
    return render_template('board_view.html', data=dict_result,)
# @app.route('/detail/<int:num>/comment', methods=['POST'])
# def add_comment(num):
#     if request.method == 'POST':
#         comment_text = request.form.get('comment_text')
#
#         # -
#         sql = "INSERT INTO comments (post_num, comment_text) VALUES (%s, %s)"
#         cursor.execute(sql, (num, comment_text))
#         conn.commit()
#
#     # 댓글을 작성한 게시글의 상세 페이지로 리다이렉트
#     return redirect(url_for('detail', num=num))

# ... (다른 라우트 및 코드 등)
@app.route('/update_board', methods=['GET', 'POST'])
def update_board():
    num_value = request.form['num']
    title_value = request.form['title']
    writer_value = request.form['writer']
    date_value = request.form['date']
    content_value = request.form['content']

    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE board_tbl SET title = %s, writer = %s, date = %s, content = %s WHERE num = %s",
            (title_value, writer_value, date_value, content_value, num_value)
        )
        conn.commit()

    return render_template('board_view.html', data=(num_value, title_value, writer_value, date_value, content_value))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)