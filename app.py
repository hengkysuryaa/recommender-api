from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://bqsesvnewrsgch:40d5730752780492a3543f146fbd295483afc6e728200c494156deac64da4d95@ec2-50-19-171-158.compute-1.amazonaws.com:5432/dcenc4qk0na3sm"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))

class Healtz(Resource):
    # Check API connection
    
    def get(self):
        return jsonify({'message':'Hello World!'})

    def post(self):
        data = request.get_json()
        return jsonify({'message':f'Hello, {data.get("name")}!'})

class Auth(Resource):

    def post(self):
        data = request.get_json()
        user = db.session.query(User).filter((User.username == data.get("username")) and (User.password == data.get("password"))).all()
        
        return jsonify({'success': bool(len(user))})

# Add new endpoint here
api.add_resource(Healtz, '/')
api.add_resource(Auth, '/auth')

# if __name__ == '__main__':
#     app.run(debug = True)