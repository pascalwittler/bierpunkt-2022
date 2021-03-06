import shelve

from flask import Flask, g
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

CORS(app)

def get_db(database_name):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open(database_name)
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return {'message': 'Hello world!', 'data': {}}, 200

class UserList(Resource):
    def get(self):
        shelf = get_db('data/users.db')
        keys = list(shelf.keys())

        users = []

        for key in keys:
            users.append(shelf[key])

        return {'message': 'Success', 'data': users}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required = True)
        parser.add_argument('firstName', required = True)
        parser.add_argument('lastName', required = True)
        parser.add_argument('email', required = True)

        args = parser.parse_args()

        shelf = get_db('data/users.db')
        shelf[args['identifier']] = args

        return {'message': 'User added', 'data': args}, 201

class User(Resource):
    def get(self, identifier):
        shelf = get_db('data/users.db')

        if not (identifier in shelf):
            return {'message': 'User not found', 'data': {}}, 404

        return {'message': 'User found', 'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_db('data/users.db')

        if not (identifier in shelf):
            return {'message': 'User not found', 'data': {}}, 404

        del shelf[identifier]
        return {'message': 'User deleted', 'data': {}}, 204

class ProductList(Resource):
    def get(self):
        shelf = get_db('data/products.db')
        keys = list(shelf.keys())

        products = []

        for key in keys:
            products.append(shelf[key])

        return {'message': 'Success', 'data': products}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required = True)
        parser.add_argument('name', required = True)
        parser.add_argument('price', type = int, required = True)

        args = parser.parse_args()

        shelf = get_db('data/products.db')
        shelf[args['identifier']] = args

        return {'message': 'Product added', 'data': args}, 201

class Product(Resource):
    def get(self, identifier):
        shelf = get_db('data/products.db')

        if not (identifier in shelf):
            return {'message': 'Product not found', 'data': {}}, 404

        return {'message': 'Product found', 'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_db('data/products.db')

        if not (identifier in shelf):
            return {'message': 'Product not found', 'data': {}}, 404

        del shelf[identifier]
        return {'message': 'Product deleted', 'data': {}}, 204

api.add_resource(UserList, '/users')
api.add_resource(User, '/user/<string:identifier>')
api.add_resource(ProductList, '/products')
api.add_resource(Product, '/product/<string:identifier>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2342, debug=True)
