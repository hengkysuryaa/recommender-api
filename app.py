from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from model import recommendation, history

app = Flask(__name__)
CORS(app)
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
    @cross_origin()
    def get(self):
        return jsonify({'message':'Hello World!'})

    @cross_origin()
    def post(self):
        data = request.get_json()
        return jsonify({'message':f'Hello, {data.get("name")}!'})

class Auth(Resource):

    @cross_origin()
    def post(self):
        data = request.get_json()
        user = db.session.query(User).filter(User.username == data.get("username")).all()
        if (len(user) != 0) and (data.get("password") == user[0].password):
            return jsonify({'success': True})
        
        return jsonify({'success': False})

class Recommend(Resource):

    @cross_origin()
    def post(self):
        data = request.get_json()
        ids, ratings, urls = recommendation(data.get("name"))
        data = []
        for i in range(len(ids)):
            item = {
                "id" : i+1,
                "product_id" : ids[i],
                "product_url" : urls[i],
                "predicted_rating" : ratings[i]
            }
            data.append(item)

        return jsonify({'data': data})

class History(Resource):

    @cross_origin()
    def post(self):
        data = request.get_json()
        ids, ratings, urls = history(data.get("name"))
        data = []
        for i in range(len(ids)):
            item = {
                "id" : i+1,
                "product_id" : ids[i],
                "product_url" : urls[i],
                "user_rating" : ratings[i]
            }
            data.append(item)

        return jsonify({'data': data})

# Add new endpoint here
api.add_resource(Healtz, '/')
api.add_resource(Auth, '/auth')
api.add_resource(Recommend, '/recommend')
api.add_resource(History, '/history')

if __name__ == '__main__':
    app.run(debug = True)