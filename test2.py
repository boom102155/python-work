from flask import Flask, jsonify, render_template, request, json
from flask_restful import Api
from sqlalchemy import create_engine

db_connect = create_engine('oracle://ADBOOM:boom125478@127.0.0.1:1521/xe')
app = Flask(__name__)

# api = Api(app)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/lend', methods = ['POST', 'GET'])
def lend():
    conn = db_connect.connect()
    query = conn.execute("SELECT to_char(lh.LEND_DATE, 'yyyy-mm-dd'), ps.NAME, ps.SURNAME, ps.FACULTY, ps.CLASS, eq.SERIAL_NUMBER, eq.EQUIPMENT_NAME "
                         "FROM LEND_HEAD lh, LEND_DETAIL ld, EQUIPMENT eq, STAFF s, PERSON ps "
                         "WHERE lh.PERSON_ID = ps.PERSON_ID AND lh.STAFF_ID = s.STAFF_ID AND lh.LEND_NO = ld.LEND_NO AND ld.EQUIPMENT_ID = eq.EQUIPMENT_ID")
    rows = query.fetchall();
    return render_template("lend.html", rows=rows)

@app.route('/equipment', methods = ['POST', 'GET'])
def equipment():
    conn = db_connect.connect()
    query1 = conn.execute("SELECT eq.EQUIPMENT_ID, "
                         "eq.EQUIPMENT_NAME, "
                         "ca.CATEGORY_NAME, "
                         "eq.CALL_NUMBER, "
                         "eq.SERIAL_NUMBER, "
                         "to_char(eq.CREATE_DATE, 'yyyy-mm-dd') "
                         "FROM EQUIPMENT eq INNER JOIN CATEGORY ca ON eq.CATEGORY_ID = ca.CATEGORY_ID")
    rows1 = query1.fetchall();

    query2 = conn.execute("SELECT CATEGORY_NAME FROM CATEGORY");
    rows2 = query2.fetchall();

    query3 = conn.execute("SELECT CATEGORY_ID, CATEGORY_NAME FROM CATEGORY")
    rows3 = query3.fetchall();



    return render_template("equipment.html", rows1=rows1 , rows2=rows2 , rows3=rows3)

@app.route('/gettest' , methods = ['POST' , 'GET'])
def gettest():
    equipname = request.get_json()
    print(equipname["cateID"])
    return json.dumps(equipname)

@app.route('/test' , methods = ['POST' , 'GET'])
def test():
    conn = db_connect.connect()
    query = conn.execute("SELECT CATEGORY_ID, CATEGORY_NAME FROM CATEGORY")
    rows = query.fetchall();
    return render_template("test.html" , rows=rows)

@app.route('/category', methods = ['POST', 'GET'])
def category():
    conn = db_connect.connect()
    query = conn.execute("SELECT "
                         "CATEGORY_ID, "
                         "CATEGORY_NAME, "
                         "SHORT_NAME, TYPE, "
                         "DETAIL, "
                         "to_char(CREATE_DATE, 'yyyy-mm-dd') FROM CATEGORY")
    rows = query.fetchall();
    return render_template("category.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)