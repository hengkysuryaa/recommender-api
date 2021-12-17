from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Healtz(Resource):
    # Check API connection
    
    def get(self):
        return jsonify({'message':'Hello World!'})

    def post(self):
        data = request.get_json()
        return jsonify({'message':f'Hello, {data.get("name")}!'})

# Add new endpoint here
api.add_resource(Healtz, '/')