from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):
	def get(self):
		return {'item': [item.json() for item in ItemModel.query.all()]}
		
class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', type = float, required = True, help = 'This field cannot be left blank')
	parser.add_argument('store_id', type = int, required = True, help = 'every item needs a store id')
	

	@jwt_required()
	def get(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			return item.json()
		return {'message': 'item not found'}, 404

	def post(self, name):
		if(ItemModel.find_by_name(name)):
			return {'message' : "item with name '{}' already exists".format(name)}, 409
		
		data = Item.parser.parse_args()
		item = ItemModel(name, **data)
		try:
			item.save_to_db()
		except:
			return {'message': "error occured while inserting the item!"}, 500
		
		return item.json(), 201
		
	def put(self, name):
		data = Item.parser.parse_args()
		item = ItemModel.find_by_name(name)

		if item:
			item.price = data['price']
			item.store_id = data['store_id']
		else:
			item = ItemModel(name, **data)
		item.save_to_db()	
		return item.json()
			

	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete_from_db()
		connection = sqlite3.connect('data.db')
		return {'message' : "item deleted"}
