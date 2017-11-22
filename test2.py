from flask import Flask, jsonify, render_template, request
from flask_restful import Api
from sqlalchemy import create_engine

db_connect = create_engine('oracle://ADBOOM:boom125478@127.0.0.1:1521/xe')
app = Flask(__name__)

# api = Api(app)

# -------------EQUIPMENT QUERY----------------

# @app.route('add_category', methods=['POST'])
# def add_category():
#     if request.method == 'POST':
#         try:
#             cateid = request.form['cateid']
#             catename = request.form['catename']
#             shortname = request.form['shortname']
#             type = request.form['type']
#             detail = request.form['detail']
#             createdate = request.form['createdate']
#             updatedate = request.form['updatedate']
#
#             conn = db_connect.connect()
#             conn.execute("INSERT INTO CATEGORY (CATEGORY_ID,CATEGORY_NAME,SHORT_NAME,TYPE,DETAIL,CREATE_DATE,UPDATE_DATE) VALUES(?, ?, ?, ?, ?, ?, ?)",
#                          (cateid, catename, shortname,type, detail, createdate, updatedate))
#
#             conn.commit()
#             msg = "Record successfully added"
#         except:
#             conn.rollback()
#             msg = "error in insert operation"
#
#         finally:
#             return render_template("category.html", msg=msg)
#             conn.close()


@app.route('/equipment')
def equipment():
    conn = db_connect.connect()
    query = conn.execute("SELECT eq.EQUIPMENT_ID, "
                         "eq.EQUIPMENT_NAME, "
                         "ca.CATEGORY_NAME, "
                         "eq.CALL_NUMBER, "
                         "eq.SERIAL_NUMBER, "
                         "eq.CREATE_DATE "
                         "FROM EQUIPMENT eq INNER JOIN CATEGORY ca ON eq.CATEGORY_ID = ca.CATEGORY_ID")
    rows = query.fetchall();
    return render_template("equipment.html", rows=rows)

@app.route('/category')
def category():
    conn = db_connect.connect()
    query = conn.execute("SELECT * FROM CATEGORY")
    rows = query.fetchall();
    return render_template("category.html", rows=rows)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)