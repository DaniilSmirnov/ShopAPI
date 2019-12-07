from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request
import mysql.connector
from flask_cors import CORS
import json
from hashlib import sha256

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin: *'

cors = CORS(app)
api = Api(app)

def get_cnx():
    cnx = mysql.connector.connect(user='root', password='',
                                  host='0.0.0.0',
                                  database='')
    return cnx


class TestConnection(Resource):
    def get(self):
        return {'status': 'success'}


class Basket(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)

        args = parser.parse_args()
        _id = args['id']

        cnx = get_cnx()

        cursor = cnx.cursor(buffered=True)

        query = "select * from order where client_id = %s and status = 'basket';"
        data = (_id, )
        response = []
        cursor.execute(query, data)
        for item in cursor:
            i = 0
            catalog = {}
            for value in item:
                if i == 0:
                    catalog.update({'id_order': value})
                if i == 1:
                    catalog.update({'itog_summ': value})
                if i == 2:
                    catalog.update({'date': value})
                if i == 3:
                    catalog.update({'status': value})
                if i == 4:
                    catalog.update({'client_id': value})
                if i == 5:
                    catalog.update({'order_col': value})
                i += 1
            response.append(catalog)
        return response

    def update(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        parser.add_argument('product_id', type=int)
        parser.add_argument('kolvo', type=int)

        args = parser.parse_args()
        _id = args['id']
        _product_id = args['product_id']
        _kolvo = args['kolvo']

        cnx = get_cnx()

        cursor = cnx.cursor(buffered=True)

        query = "select id_order from order where client_id = %s and status = 'basket'"
        data = (_id, )
        cursor.execute(query, data)
        for item in cursor:
            for value in item:
                id_order = value

        query = "insert into structure values (%s, %s, %s)"
        data = (_product_id, id_order, _kolvo)

        cursor.execute(query, data)
        cnx.commit()

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        args = parser.parse_args()
        _id = args['id']


        cnx = get_cnx()

        cursor = cnx.cursor(buffered=True)

        query = "select id_order from order where client_id = %s and status = 'basket'"
        data = (_id, )
        cursor.execute(query, data)
        for item in cursor:
            for value in item:
                id_order = value

        query = "delete from structure where id_order = %s;"
        data = (id_order)
        cursor.execute(query, data)
        cnx.commit()
        return {'success': True}


class GetСatalog(Resource):
    def get(self):
        try:
            cnx = get_cnx()

            cursor = cnx.cursor(buffered=True)
            query = "select id_product, category_id, image, name_product from product;"

            response = []
            cursor.execute(query)
            for item in cursor:
                i = 0
                catalog = {}
                for value in item:
                    if i == 0:
                        catalog.update({'product_id': value})
                    if i == 1:
                        catalog.update({'category_id': value})
                    if i == 2:
                        catalog.update({'image': value})
                    if i == 3:
                        catalog.update({'product_name': value})
                    i += 1
                response.append(catalog)
            return response
        except BaseException as e:
            return str(e)


class UserGet(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hash', type=str)

        args = parser.parse_args()
        _hash = args['hash']

        cnx = get_cnx()

        cursor = cnx.cursor(buffered=True)

        query = 'select login, pass where hash = %s;'
        data = (_hash, )
        cursor.execute(query, data)
        i = 0
        for item in cursor:
            for value in item:
                if i == 0:
                    log = value
                if i == 1:
                    password = value
                i += 1

        hash = str(log) + str(password)
        hash = sha256(hash).hexdigest()
        if hash == _hash:
            return {'success': 'true'}


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('group', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('hash', type=str)

        args = parser.parse_args()
        _login = args['login']
        _password = args['password']
        _group = args['_group']
        _date = args['date']
        _name = args['name']
        _surname = args['surname']
        _hash = args['hash']


        cnx = get_cnx()

        cursor = cnx.cursor(buffered=True)

        query = "insert into client values (default, %s, %s, %s, %s, %s, %s, %s)"
        data = (_password, _group, _login, _name, _surname, _date, _hash)
        cursor.execute(query, data)

        return {'success': 'true'}


api.add_resource(TestConnection, '/TestConnection')
api.add_resource(Basket, '/Basket')
api.add_resource(GetСatalog, '/GetCatalog')
api.add_resource(UserGet, '/UserGet')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')