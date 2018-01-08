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
    query1 = conn.execute("SELECT lh.LEND_NO, "
                          "to_char(lh.LEND_DATE, 'yyyy-mm-dd'), "
                          "(s.NAME || ' ' || "
                          "s.SURNAME), "
                          "(ps.NAME || ' ' || "
                          "ps.SURNAME), "
                          "ps.FACULTY, "
                          "ps.CLASS, "
                          "eq.EQUIPMENT_ID, "
                          "eq.SERIAL_NUMBER, "
                          "eq.EQUIPMENT_NAME "
                         "FROM LEND_HEAD lh, LEND_DETAIL ld, EQUIPMENT eq, STAFF s, PERSON ps "
                         "WHERE lh.PERSON_ID = ps.PERSON_ID AND lh.STAFF_ID = s.STAFF_ID AND lh.LEND_NO = ld.LEND_NO AND ld.EQUIPMENT_ID = eq.EQUIPMENT_ID")
    rows1 = query1.fetchall();

    query2 = conn.execute("SELECT EQUIPMENT_ID, EQUIPMENT_NAME FROM EQUIPMENT")
    rows2 = query2.fetchall();

    return render_template("lend.html", rows1=rows1, rows2=rows2)

@app.route('/addinspection', methods = ['POST', 'GET'])
def addinspection():
    try:
        data = request.get_json()
        conn = db_connect.connect()
        conn.execute("INSERT INTO LEND_INSPECTION (LEND_NO, INSPECTION_DATE, INSPECTION_STATUS, STAFF_ID, CREATE_DATE, UPDATE_DATE) "
                     "VALUES (:1, TO_DATE(:2, 'yyyy-mm-dd'), :3, :4, TO_DATE(:5, 'yyyy-mm-dd'), TO_DATE(:6, 'yyyy-mm-dd'))",
                     (data["lendno"], data["inspdate"], data["sta"], data["staff"], data["createdate"], data["update"]))

        conn.execute("INSERT INTO INSPECTION_DETAIL (LEND_NO, EQUIPMENT_ID, INSPECTION, CREATE_DATE, UPDATE_DATE) "
                     "VALUES (:1, :2, :3, TO_DATE(:4, 'yyyy-mm-dd'), TO_DATE(:5, 'yyyy-mm-dd'))",
                     (data["lendno"], data["leid"], data["inspection"], data["createdate"], data["update"]))
        conn.commit()
    except:
        conn.rollback()
    finally:
        return json.dumps(data)
        conn.close()

@app.route('/equipment', methods = ['POST', 'GET'])
def equipment():
    conn = db_connect.connect()
    query1 = conn.execute("SELECT eq.EQUIPMENT_ID, "
                         "eq.EQUIPMENT_NAME, "
                         "ca.CATEGORY_NAME, "
                         "ca.CATEGORY_ID, "
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

@app.route('/addequipment' , methods = ['POST' , 'GET'])
def addequipment():
    try:
        data = request.get_json()
        conn = db_connect.connect()
        conn.execute("INSERT INTO EQUIPMENT "
                     "(EQUIPMENT_NAME, "
                     "CATEGORY_ID, "
                     "CALL_NUMBER, "
                     "SERIAL_NUMBER, "
                     "CREATE_DATE, "
                     "UPDATE_DATE) "
                     "VALUES (:2, :3, :4, :5, to_date(:7, 'yyyy-mm-dd'), to_date(:8, 'yyyy-mm-dd'))",
                     (data["equipname"], data["cateID"], data["callnumber"], data["serialnumber"], data["createdate"], data["update"]))
        conn.commit()
    except:
        conn.rollback()
    finally:
        return json.dumps(data)
        conn.close()

@app.route('/delequipment' , methods = ['POST' , 'GET'])
def delequipment():
    data = request.get_json()
    conn = db_connect.connect()
    conn.execute("DELETE FROM EQUIPMENT WHERE EQUIPMENT_ID = "+ (data["equipmentid"]))
    return json.dumps(data)

@app.route('/editequipment' , methods = ['POST' , 'GET'])
def editequipment():
    data = request.get_json()
    conn = db_connect.connect()
    conn.execute("UPDATE EQUIPMENT "
                 "SET EQUIPMENT_NAME = '" + (data["equipname"]) + "', " +
                 "CATEGORY_ID = " + (data["cateID"]) + ", " +
                 "CALL_NUMBER = '" + (data["callnumber"]) + "', " +
                 "SERIAL_NUMBER = '" + (data["serialnumber"]) + "', " +
                 "UPDATE_DATE = " + "to_date('"+(data["update"])+"','yyyy-mm-dd')" +
                 " WHERE EQUIPMENT_ID = " + (data["equipmentid"]))
    conn.commit()
    return json.dumps(data)

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

@app.route('/addcategory', methods = ['POST', 'GET'])
def addcategory():
    try:
        data = request.get_json()
        conn = db_connect.connect()
        print(data["categoryname"], data["shortname"], data["categorytype"], data["detail"], data["createdate"], data["update"])
        conn.execute("INSERT INTO CATEGORY "
                     "(CATEGORY_ID, "
                     "CATEGORY_NAME, "
                     "SHORT_NAME, "
                     "TYPE, "
                     "DETAIL, "
                     "CREATE_DATE, "
                     "UPDATE_DATE) "
                     "VALUES (:1, :2, :3, :4, :5, to_date(:6, 'yyyy-mm-dd'), to_date(:7, 'yyyy-mm-dd'))",
                     (data["cateid"], data["categoryname"], data["shortname"], data["categorytype"], data["detail"], data["createdate"], data["update"]))
        conn.commit()
    except:
        conn.rollback()
    finally:
        return json.dumps(data)
        conn.close()

@app.route('/delcategory' , methods = ['POST' , 'GET'])
def delcategory():
    data = request.get_json()
    conn = db_connect.connect()
    conn.execute("DELETE FROM CATEGORY WHERE CATEGORY_ID = "+ (data["categoryid"]))
    return json.dumps(data)

@app.route('/editcategory' , methods = ['POST' , 'GET'])
def editcategory():
    data = request.get_json()
    conn = db_connect.connect()
    conn.execute("UPDATE CATEGORY "
                 "SET CATEGORY_ID = " + (data["cateid"]) + ", " +
                 "CATEGORY_NAME = '" + (data["categoryname"]) + "', " +
                 "SHORT_NAME = '" + (data["shortname"]) + "', " +
                 "TYPE = '" + (data["categorytype"]) + "', " +
                 "DETAIL = '" + (data["detail"]) + "', " +
                 "UPDATE_DATE = " + "to_date('"+(data["update"])+"','yyyy-mm-dd')" +
                 " WHERE CATEGORY_ID = " + (data["cateid"]))
    conn.commit()
    return json.dumps(data)

@app.route('/addlend' , methods = ['POST' , 'GET'])
def addlend():

    data = request.get_json()
    conn = db_connect.connect()

    conn.execute("INSERT INTO PERSON (PERSON_ID, NAME, SURNAME, TYPE, FACULTY, CLASS) "
                 "VALUES (:1, :2, :3, :4, :5, :6)",
                 (data["pid"], data["pname"], data["psurname"], data["pstatus"], data["pfaculty"], data["pclass"]))

    conn.execute("INSERT INTO LEND_HEAD (PERSON_ID, STAFF_ID, LEND_DATE, DETAIL, CREATE_DATE, UPDATE_DATE) "
                 "VALUES (:1, :2, TO_DATE(:3, 'yyyy-mm-dd'), :4, TO_DATE(:5, 'yyyy-mm-dd'), TO_DATE(:6, 'yyyy-mm-dd'))",
                 (data["pid"], data["sid"], data["ldate"], data["ldetail"], data["cdate"], data["udate"]))

    conn.execute("INSERT INTO LEND_DETAIL (LEND_NO, EQUIPMENT_ID, CREATE_DATE, UPDATE_DATE) "
                 "SELECT MAX(LEND_NO)as LEND_NO, :3, TO_DATE(:4, 'yyyy-mm-dd'), TO_DATE(:5, 'yyyy-mm-dd') FROM LEND_HEAD",
                 (data["eid"], data["cdate"], data["udate"]))
    conn.commit()
    return json.dumps(data)



if __name__ == '__main__':
    app.run(debug=True)

