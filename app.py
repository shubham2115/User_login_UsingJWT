from flask import Flask, jsonify, request, make_response
from flask_mongoengine import MongoEngine
from flask_restful import Api, Resource
from routes import Login, Registration, Logout,Home


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'
api = Api(app)

# connecting with database
app.config['MONGODB_SETTINGS'] = {
    'db': 'Users',
}

db = MongoEngine(app)


# -------------------EndPoints---------------------------------

api.add_resource(Registration, '/Register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Home, '/')


if __name__ == "__main__":
    app.run(debug=True, port=90)
