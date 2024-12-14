from flask import Blueprint, jsonify, request

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/api/greet', methods=['GET'])
def greet():
    name = request.args.get('name', 'World')
    return jsonify({"message": f"Hello, {name}!"})
