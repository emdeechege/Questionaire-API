from flask import jsonify, Blueprint, request, json, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ..utils.validators import Validation
from ..models.auth_models import Users


v1_auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1')

user = Users()
validator = Validation()


@v1_auth_blueprint.route('/signup', methods=['POST'])
def signup():
    """View that controls creation of new users"""
    try:
        data = request.get_json()
    except:
        return jsonify({
            "status": 400,
            "message": "Invalid input"
        }), 400

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    othername = data.get('othername')
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')
    username = data.get('username')
    isAdmin = data.get('isAdmin')
    password = data.get('password')

    """ Check for empty inputs"""
    if not all(field in data for field in ["firstname", "othername", "email", "phoneNumber", "username", "isAdmin", "password"]):
        return jsonify({
            "status": 400,
            "message": "Please fill in all the required input fields"}), 400

    if not validator.validate_phoneNumber(phoneNumber):
        return jsonify({
            "status": 400,
            "message": "Please input valid phone number"
        }), 400

    if validator.validate_password(password):
        return jsonify({
            "status": 400,
            "message": "Password not valid"
        }), 400

    if not validator.validate_email(email):
        return jsonify({
            "status": 400,
            "message": "Invalid email"
        }), 400

    if validator.username_exists(username):
        return jsonify({
            "status": 400,
            "message": "Username exists"
        }), 400

    if validator.email_exists(email):
        return jsonify({
            "status": 400,
            "message": "Email exists"
        }), 400

    password = generate_password_hash(
        password, method='pbkdf2:sha256', salt_length=8)

    res = user.signup(
        firstname, lastname, othername, email, phoneNumber, username, isAdmin, password)
    return jsonify({
        "status": 201,
        "data": [{
            "firstname": firstname,
            "lastname": lastname,
            "othername": othername,
            "email": email,
            "phoneNumber": phoneNumber,
            "username": username,
            "isAdmin": isAdmin,
        }]
    }), 201


@v1_auth_blueprint.route('/login', methods=['POST'])
def login():
    """ A view to control users login """
    try:
        data = request.get_json()
    except:
        return make_response(jsonify({
            "status": 400,
            "message": "Wrong input"
        })), 400
    username = data.get('username')
    password = data.get('password')

    if not username:
        return make_response(jsonify({
            "status": 400,
            "message": "Username is required"
        })), 400
    if not password:
        return make_response(jsonify({
            "status": 400,
            "message": "Password is required"
        })), 400

    if not validator.username_exists(username):
        return jsonify({
            "status": 404,
            "message": "User does not exist"
        }), 404

    auth_token = user.generate_auth_token(username)
    return make_response(jsonify({
        "status": 200,
        "message": 'Logged in successfuly',
        "token": auth_token
    })), 200
