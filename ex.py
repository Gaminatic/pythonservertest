import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

data = [
    {"id": 1, "name": "abc1", "message": "Hello"},
    {"id": 2, "name": "abc2", "message": "Hey"},
]


@app.route('/getUsers', methods=['GET'])
def get_items():
    time = datetime.datetime.now().isoformat()
    return jsonify({"Users": data,"time":time}), 200

@app.route('/createUsers', methods=['POST'])
def create_item():
    new_user = request.json
    user=data.append(new_user)
    print("User data",user)
    return jsonify({"message": "User created", "User": new_user}), 201

if __name__ == '__main__':
    app.run(debug=True)
