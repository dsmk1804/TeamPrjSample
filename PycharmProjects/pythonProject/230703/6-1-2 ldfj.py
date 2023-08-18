from flask import Flask,request
from TE import tree


app = Flask(__name__)

@app.route("/")
def index():
    alchol = request.args.get("alcohol")
    sugar = request.args.get("sugar")
    pH = request.args.get("pH")

    if alchol :
        predValue = tree.rfclf.predict([[float(alchol), float(sugar), float(pH)]])
        return predValue
    else:
        return "예측값을 입력하세요."

app.run(debug=True)