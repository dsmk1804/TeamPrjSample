from flask import Flask, Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:1234@localhost:3306/kcs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app, engine_options={"connect_args": {"charset": "utf8"}})

page_bp = Blueprint('match', __name__, url_prefix='/')

# 파일 업로드
@page_bp.route('/uploads', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        if f:
            filename = secure_filename(f.filename)
            f.save('static/uploads/' + filename)

            try:
                with db.engine.connect() as conn:
                    # 파일명과 파일경로를 데이터베이스에 저장함
                    sql = "INSERT INTO images (image_name, image_dir) VALUES (%s, %s)"
                    conn.execute(sql, (secure_filename(f.filename), 'uploads/' + filename))
                return '파일 업로드가 성공했습니다'
            except Exception as e:
                return 'uploads failed'
        else:
            return 'No file uploaded'

    return 'Invalid request method'

# 메인 페이지
# @page_bp.route('/')
# def page():
#     try:
#         with db.engine.connect() as conn:
#             # 이미지 정보를 데이터베이스에서 가져옴
#             sql = "SELECT image_name, image_dir FROM images"
#             data = conn.execute(sql).fetchall()
#
#         data_list = []
#
#         for obj in data:
#             data_dic = {
#                 'name': obj[0],
#                 'dir': obj[1]
#             }
#             data_list.append(data_dic)
#
#         return render_template('index.html', data_list=data_list)
#     except Exception as e:
#         return 'An error occurred while fetching data from the database'


# 다른 방법
# 해당 코드는 파일 업로드 테스트하기 위한 임시 코드임
# 업로드된 파일을 저장할 경로 설정
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 업로드된 파일 가져오기
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            # 파일 저장 경로 설정
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # 파일 저장
            uploaded_file.save(file_path)
            return 'File uploaded successfully!'
    return render_template('index.html')

app.register_blueprint(page_bp)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")



