from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request
import mysql.connector
from flask_cors import CORS
import json

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin: *'

cors = CORS(app)
api = Api(app)


class TestConnection(Resource):
    def get(self):
        return {'status': 'success'}


class AddMeet(Resource):
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('owner_id', type=int)
        parser.add_argument('sig', type=int)
        parser.add_argument('start', type=str)
        parser.add_argument('finish', type=str)
        parser.add_argument('photo', type=str)
        args = parser.parse_args()

        _name = args['name']
        _signature = args['sig']
        _description = args['description']
        _owner_id = args['owner_id']
        _start = args['start']
        _finish = args['finish']
        _photo = args['photo']

        try:
            cnx = mysql.connector.connect(user='root', password='misha_benich228',
                                          host='0.0.0.0',
                                          database='meets')

            cursor = cnx.cursor(buffered=True)
            query = "select sig from members where idmembers = %s and sig = %s"
            data = (_owner_id, _signature,)
            cursor.execute(query, data)

            for item in cursor:
                for value in item:
                    if str(value) == str(_signature):
                        query = "insert into meetings values (default, %s, %s, %s, default, %s, %s, default, %s)"
                        data = (_name, _description, _owner_id, _start, _finish, _photo)
                        cursor.execute(query, data)
                        cnx.commit()
                        return {'success': True}
                    else:
                        return {'failed': '403'}

            return {'success': True}

        except BaseException as e:
            return {'error' : str(e)}


class Basket(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)

        args = parser.parse_args()
        _id = args['id']

        cnx = mysql.connector.connect(user='root', password='',
                                      host='0.0.0.0',
                                      database='')

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

        cnx = mysql.connector.connect(user='root', password='',
                                      host='0.0.0.0',
                                      database='')

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


        cnx = mysql.connector.connect(user='root', password='',
                                      host='0.0.0.0',
                                      database='')

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
            cnx = mysql.connector.connect(user='root', password='',
                                          host='0.0.0.0',
                                          database='')

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
        _id = args['id']

        cnx = mysql.connector.connect(user='root', password='',
                                      host='0.0.0.0',
                                      database='')

        cursor = cnx.cursor(buffered=True)
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hash', type=str)

        args = parser.parse_args()
        _id = args['id']

        cnx = mysql.connector.connect(user='root', password='',
                                      host='0.0.0.0',
                                      database='')

        cursor = cnx.cursor(buffered=True)
        
# TODO: регистрация, авторизация, корзина(удаление)


api.add_resource(TestConnection, '/TestConnection')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')