from flask import Flask,render_template, request, jsonify
import random

app = Flask(__name__)

# 初始化遊戲變量
a = random.randint(1, 20)
b = random.randint(100, 150)
data = random.randint(a, b)
attempts = 5

@app.route('/start', methods=['GET'])
def start_game():
    global a, b, data, attempts
    a = random.randint(1, 20)
    b = random.randint(100, 150)
    data = random.randint(a, b)
    attempts = 6
    return jsonify({"range": f"{a}~{b}", "attempts": attempts})

@app.route('/guess', methods=['POST'])
def guess():
    global attempts, a, b, data
    if attempts > 0:
        guess = request.json.get('guess')
        guess = int(guess)
        attempts -= 1

        response = {}
        if guess < data:
            if guess >= a:
                a = guess + 1
                response = {"message": f"{guess}~{b}"}
            else:
                response = {"message": "再想想"}
        elif guess > data:
            if guess <= b:
                b = guess - 1
                response = {"message": f"{a}~{guess}"}
            else:
                response = {"message": "再想想"}
        else:
            response = {"message": "恭喜答對！", "correct": True}

        if attempts == 0 and guess != data:
            response = {"message": f"遊戲結束。正確的數字是{data}。再接再厲！", "correct": False}
        elif attempts > 0:
            response["attempts"] = attempts  # 只有在還有剩餘次數時才回傳

        return jsonify(response)
    else:
        return jsonify({"message": "沒有剩餘嘗試次數。"})

@app.route('/')
def rander():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
