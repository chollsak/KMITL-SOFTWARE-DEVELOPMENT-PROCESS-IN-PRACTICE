from flask import Flask, jsonify, request
import re

app = Flask(__name__)

# In-memory database simulation
users = {}

# GET /user/ - List all registered users
@app.route('/user/', methods=['GET'])
def list_users():
    return jsonify(users), 200

# POST /user/new - Create a new user
@app.route('/user/new', methods=['POST'])
def create_user():
    data = request.json
    if not data or 'username' not in data or 'minlen' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    username = data['username']
    minlen = data['minlen']
    
    try:
        if not is_valid_username(username, minlen):
            return jsonify({"error": "Invalid username"}), 400
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    
    user_id = len(users) + 1
    users[user_id] = {"id": user_id, "username": username}
    return jsonify({"id": user_id}), 201

# PUT /user/<user_id> - Update an existing user
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if not data or 'username' not in data or 'minlen' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    username = data['username']
    minlen = data['minlen']
    
    try:
        if not is_valid_username(username, minlen):
            return jsonify({"error": "Invalid username"}), 400
    except (TypeError, ValueError) as e:
        return jsonify({"error": str(e)}), 400

    users[user_id]['username'] = username
    return jsonify({"message": "User updated successfully"}), 200

# GET /user/<user_id> - Get details of a user
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify(users[user_id]), 200

# DELETE /user/<user_id> - Delete a user
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted successfully"}), 200


def is_valid_date(date_str):
    if not date_str or len(date_str) != 10:
        return False

    try:
        year, month, day = map(int, date_str.split("-"))
        if year < 1000 or year > 9999:
            return False
        if month < 1 or month > 12:
            return False

        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month == 2:  # Check for leap year
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                days_in_month[1] = 29
        if day < 1 or day > days_in_month[month - 1]:
            return False

    except ValueError:
        return False

    return True


def is_valid_username(username, minlen):
    if type(username) != str:
        raise TypeError("username must be a string")

    if minlen < 1:
        raise ValueError("minlen must be at least 1")

    if len(username) < minlen:
        return False

    if not re.match('^[a-z0-9._]*$', username):
        return False

    if username[0].isnumeric():
        return False

    return True


if __name__ == '__main__':
    app.run(debug=True)
