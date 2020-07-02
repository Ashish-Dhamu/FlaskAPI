import sqlite3
from flask import request
from flask_restful import reqparse, Resource
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can not be left blank")
    
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="This field can not be left blank")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'error message': 'the item: {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {"message": "Item has been deleted!"}

    def put(self, name):

        data = Item.parser.parse_args()
        

        # if ItemModel.find_by_name(name) is None:
        item = ItemModel(name,**data)
        # else:
        #
        #     item.price = data["price"]
        #     item.store_id = data["store_id"]
        
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda row: row.json(), ItemModel.query.all()))}
