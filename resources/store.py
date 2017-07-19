from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	#parser = reqparse.RequestParser()
	#parser.add_argument('name', type = str, required = True, help = "This field cannot leave blank")
	
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json()
		return {'message': 'store not found'}, 404
		
	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': "A store with name '{}' already exists".format(name)}, 409
		
		#data = Store.parser.parse_args()
		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message': 'An error occured while inserting store'}, 500
		
		return store.json(), 201
		
	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
		return {'message': "store deleted"}


class StoreList(Resource):
	def get(self):
		return {"stores": [x.json() for x in StoreModel.query.all()]}
