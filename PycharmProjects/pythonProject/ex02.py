from flask import Flask, render_template, request
import ex01

app = Flask(__name__)

@app.route("/")
def index():
    return "index"

@app.route("/aa",methods=['GET','POST'])
def aa():
    result = 10
    if request.method == 'POST':
        x = request.form['x']
        y = request.form['y']
        result = ex01.doA(int(x),int(y))
    # 위의 () 안의 숫자를 한번 바꿔보세요
    elif request.method == 'GET':
        print("GET")
    return render_template("aa.html", result=result)

app.run(host='127.0.0.1',debug=True)

# 호스트 127.0.0.1 을 불러내는 과정
# 밑에 Running on ~~ 뜨면 성공임