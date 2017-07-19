import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'username', type = str, required = True, help = 'This field cannot be left blank'
	)				
	parser.add_argument(
		'password', type = str, required = True, help = 'This field cannot be left blank'
	)
				
	def post(self):
		data = UserRegister.parser.parse_args()	
		user = UserModel.find_by_name(data['username'])
			
	
		if user:
			return {'message' : "user with the same name already exists"}, 409
	
		user = UserModel(**data)
		user.save_to_db()
		
		return {'message': 'User successfully created'}, 201
