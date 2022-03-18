from flask_restful import Resource
from flask import request, jsonify, session, make_response
from model import Users
from Utils import token_required, get_token, url_short


class Home(Resource):
    @token_required
    def get(user_name):
        data = Users.objects(UserName=user_name).first()
        return jsonify(message=f'Hello {data.Name}', UserName=f'{data.UserName}', Email=f'{data.Email}')


class Logout(Resource):
    def get(self):
        user = session['Name']
        session['logged_in'] = False
        return make_response(jsonify(message='Logged Out'), 200)


class Registration(Resource):
    def post(self):
        data_ = Users.objects()
        username = request.form.get('UserName')
        name = request.form.get('Name')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')
        session['logged_in'] = False
        if not password2 == password1:
            return make_response(jsonify(message='Password1 and Password2 must be same'), 409)
        data = Users(UserName=username, Name=name, Email=email, Password=password1)
        for itr in data_:
            if itr.UserName == data.UserName:
                return make_response(jsonify(message='UserName Already Taken'), 409)
        data.save()
        return make_response(jsonify(message='User Created Check your registered Email to activate account'), 200)


class Login(Resource):
    def post(self):
        if not session['logged_in']:
            user_name = request.form.get('UserName')
            password = request.form.get('Password')
            data_ = Users.objects(UserName=user_name).first()
            if data_:
                if password == data_.Password:
                    session['logged_in'] = True
                    session['Name'] = data_.Name
                    token = get_token(user_name)
                    short_token = url_short(token)
                    return {"message": "you are logged in",
                            "token": short_token}

                return make_response(jsonify(message='You have entered wrong Password'), 404)
            else:
                return make_response(jsonify(message='Entered User name not exist'))
        else:
            return make_response(jsonify(message=f"{session['Name']} is already logged in"), 409)
