from flask import Flask, jsonify, request, render_template
from flask.wrappers import Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask import jsonify


db_connect = create_engine('oracle://ADBOOM:boom125478@127.0.0.1:1521/xe')
app = Flask(__name__)

api = Api(app)

# -------------EQUIPMENT QUERY----------------

class Equipment(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM EQUIPMENT")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Add_Equipment(Resource):
    def get(self, EQUIPMENT_ID, EQUIPMENT_NAME, CATEGORY_ID, CALL_NUMBER, SERIAL_NUMBER, PATH_PIC, CREATE_DATE, UPDATE_DATE):
        conn = db_connect.connect()
        query = conn.execute("INSERT INTO EQUIPMENT "
                             "(EQUIPMENT_ID, "
                             "EQUIPMENT_NAME, "
                             "CATEGORY_ID, "
                             "CALL_NUMBER, "
                             "SERIAL_NUMBER, "
                             "PATH_PIC, "
                             "CREATE_DATE, "
                             "UPDATE_DATE) "
                             "VALUES (%d,%s,%d,%s,%s,%s,%s,%s)", (EQUIPMENT_ID, EQUIPMENT_NAME, CATEGORY_ID, CALL_NUMBER, SERIAL_NUMBER, PATH_PIC, CREATE_DATE, UPDATE_DATE))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Delete_Equipment(Resource):
     def get(self, EQUIPMENT_ID):
         conn = db_connect.connect()
         query = conn.execute("DELETE FROM EQUIPMENT WHERE EQUIPMENT_ID =%d" %int(EQUIPMENT_ID))
         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
         return jsonify(result)

class Update_Equipment(Resource):
     def get(self, EQUIPMENT_ID):
         conn = db_connect.connect()
         query = conn.execute("UPDATE EQUIPMENT SET EQUIPMENT_NAME = ,"
                              "CATEGORY_ID = ,"
                              "CALL_NUMBER = ,"
                              "SERIAL_NUMBER = ,"
                              "PATH_PIC = ,"
                              "UPDATE_DATE = "
                              "[WHERE EQUIPMENT_ID =%d]" %int(EQUIPMENT_ID))
         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
         return jsonify(result)

# -------------CATEGORY QUERY----------------

class Category(Resource):
     def get(self):
         conn = db_connect.connect()
         query = conn.execute("SELECT * FROM CATEGORY")
         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
         return jsonify(result)

class Add_Category(Resource):
     def get(self, CATEGORY_NAME, SHORT_NAME, TYPE, DETAIL, CREATE_DATE, UPDATE_DATE):
         conn = db_connect.connect()
         query = conn.execute("INSERT INTO CATEGORY "
                              "(CATEGORY_NAME,"
                              "SHORT_NAME,"
                              "TYPE,"
                              "DETAIL,"
                              "CREATE_DATE,"
                              "UPDATE_DATE)"
                              "VALUES (%s,%s,%s,%s,%s,%s)", (CATEGORY_NAME, SHORT_NAME, TYPE, DETAIL, CREATE_DATE, UPDATE_DATE))
         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
         return jsonify(result)

class Delete_Category(Resource):
    def get(self, CATEGORY_ID):
        conn = db_connect.connect()
        query = conn.execute("DELETE FROM CATEGORY WHERE CATEGORY_ID =%d" % int(CATEGORY_ID))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Update_Category(Resource):
     def get(self, CATEGORY_ID):
         conn = db_connect.connect()
         query = conn.execute("UPDATE EQUIPMENT SET CATEGORY_NAME = ,"
                              "SHORT_NAME = ,"
                              "TYPE = ,"
                              "DETAIL = ,"
                              "UPDATE_DATE = "
                              "[WHERE CATEGORY_ID =%d]" %int(CATEGORY_ID))
         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
         return jsonify(result)

class Lend_Head(Resource):
     def get(self):
         conn = db_connect.connect()
         query = conn.execute("SELECT * FROM LEND_HEAD")
         return {'LEND_HEAD': [i[0] for i in query.cursor.fetchall()]}

class Add_Lend_Head(Resource):
     def get(self, PERSON_ID, STAFF_ID, LEND_DATE, DETAIL, CREATE_DATE, UPDATE_DATE):
         conn = db_connect.connect()
         query = conn.execute("INSERT INTO LEND_HEAD "
                              "(PERSON_ID,"
                              "STAFF_ID,"
                              "LEND_DATE,"
                              "DETAIL,"
                              "CREATE_DATE,"
                              "UPDATE_DATE)"
                              "VALUES (%d,%d,%s,%s,%s,%s)", (PERSON_ID, STAFF_ID, LEND_DATE, DETAIL, CREATE_DATE, UPDATE_DATE))
         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
         return jsonify(result)

class Add_Lend_Detail(Resource):
    def get(self, LEND_NO, SEQ_NO, EQUIPMENT_ID, CREATE_DATE, UPDATE_DATE):
        conn = db_connect.connect()
        query = conn.execute("INSERT INTO LEND_DETAIL"
                             "(LEND_NO,"
                             "SEQ_NO,"
                             "EQUIPMENT_ID,"
                             "CREATE_DATE,"
                             "UPDATE_DATE)"
                             "VALUES (%d,%d,%d,%s,%s)", (LEND_NO, SEQ_NO, EQUIPMENT_ID, CREATE_DATE, UPDATE_DATE))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(Equipment, '/equipment')
api.add_resource(Add_Equipment, '/add_equipment')
api.add_resource(Delete_Equipment, '/delete_equipment')
api.add_resource(Update_Equipment, '/update_equipment')

api.add_resource(Category, '/category')
api.add_resource(Add_Category, '/add_category')
api.add_resource(Delete_Category, '/delete_category')
api.add_resource(Update_Category, '/update_category')

api.add_resource(Lend_Head, '/lend_head')
api.add_resource(Add_Lend_Head, '/add_lend_equipment')
api.add_resource(Add_Lend_Detail, '/add_lend_detail')

if __name__ == '__main__':
    app.run(debug=True)