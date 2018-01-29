from flask import Flask, jsonify, render_template, request, json, redirect, url_for
from sqlalchemy import create_engine

db_connect = create_engine('oracle://ADBOOM:boom125478@127.0.0.1:1521/xe')
app = Flask(__name__)

datareport = {}
# api = Api(app)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginsubmit' , methods = ['POST' , 'GET'])
def loginsubmit():
    data = request.get_json()
    conn = db_connect.connect()
    query = conn.execute("SELECT NAME, SURNAME FROM STAFF "
                         "WHERE USER_NAME = '" + (data["user"]) + "'" +
                         " AND PASSWORD = '" + (data["pass"]) + "'")
    rows = query.fetchall()
    for row in rows:
        list1 = ["NAME", "SURNAME"]
        list2 = [row["name"], row["surname"]]
        data = zip(list1, list2)
        d = dict(data)
        print(d)

    return jsonify(d)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/lend', methods = ['POST' , 'GET'])
def lend():
    conn = db_connect.connect()
    query1 = conn.execute("SELECT tb.lend_no, "
                          "tb.lenddate, "
                          "tb.staff, "
                          "tb.person, "
                          "tb.type, "
                          "tb.faculty, "
                          "tb.class, "
                          "tb.equipment_id, "
                          "tb.serial_number, "
                          "tb.equipment_name, "
                          "nvl2(li.lend_no,'คืนแล้ว','ยังไม่ได้คืน') as status "
                          "FROM (SELECT lh.lend_no, "
                          "TO_CHAR(lh.lend_date,'yyyy-mm-dd') AS lenddate, "
                          "(s.name || ' ' || s.surname ) AS staff, "
                          "(ps.name || ' ' || ps.surname ) AS person, "
                          "ps.type, "
                          "ps.faculty, "
                          "ps.class, "
                          "eq.equipment_id, "
                          "eq.serial_number, "
                          "eq.equipment_name "
                          "FROM "
                          "lend_head lh, "
                          "lend_detail ld, "
                          "equipment eq, "
                          "staff s, "
                          "person ps "
                          "WHERE "
                          "lh.person_id = ps.person_id "
                          "AND   lh.staff_id = s.staff_id "
                          "AND   lh.lend_no = ld.lend_no "
                          "AND   ld.equipment_id = eq.equipment_id) tb "
                          "LEFT JOIN lend_inspection li ON li.lend_no = tb.lend_no")
    rows1 = query1.fetchall()

    query2 = conn.execute("SELECT EQUIPMENT_ID, EQUIPMENT_NAME FROM EQUIPMENT")
    rows2 = query2.fetchall()

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
    query1 = conn.execute("SELECT te.equipment_id, "
                          "te.equipment_name, "
                          "c.CATEGORY_NAME, "
                          "te.CATEGORY_ID, "
                          "te.CALL_NUMBER, "
                          "te.SERIAL_NUMBER, "
                          "te.summary "
                          "FROM CATEGORY c , TB_EQUIP te "
                          "WHERE c.CATEGORY_ID = te.CATEGORY_ID")
    rows1 = query1.fetchall()

    query2 = conn.execute("SELECT CATEGORY_NAME FROM CATEGORY")
    rows2 = query2.fetchall()

    query3 = conn.execute("SELECT CATEGORY_ID, CATEGORY_NAME FROM CATEGORY")
    rows3 = query3.fetchall()

    return render_template("equipment.html", rows1=rows1 , rows2=rows2 , rows3=rows3)

@app.route('/addequipment' , methods = ['POST' , 'GET'])
def addequipment():
    try:
        data = request.get_json()
        conn = db_connect.connect()
        conn.execute("INSERT INTO EQUIPMENT "
                     "(EQUIPMENT_ID, "
                     "EQUIPMENT_NAME, "
                     "CATEGORY_ID, "
                     "CALL_NUMBER, "
                     "SERIAL_NUMBER, "
                     "CREATE_DATE, "
                     "UPDATE_DATE, "
                     "QTY) "                   
                     "VALUES (EQUIPMENT_SEQ.NEXTVAL, :2, :3, :4, :5, to_date(:7, 'yyyy-mm-dd'), to_date(:8, 'yyyy-mm-dd'), :9)",
                     (data["equipname"], data["cateID"], data["callnumber"], data["serialnumber"], data["createdate"], data["update"], data["eqty"]))
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
                 "UPDATE_DATE = " + "to_date('"+(data["update"])+"','yyyy-mm-dd')," +
                 "QTY = " + (data["quantity"]) +
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
                         "DETAIL "
                         "FROM CATEGORY")
    rows = query.fetchall()
    return render_template("category.html", rows=rows)

@app.route('/addcategory', methods = ['POST', 'GET'])
def addcategory():
    try:
        data = request.get_json()
        conn = db_connect.connect()
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
    conn.execute("MERGE INTO PERSON P USING (SELECT " + (data["pid"]) + " PERSON_ID," +
                                             "'" + (data["pname"]) + "' NAME," +
                                             "'" + (data["psurname"]) + "' SURNAME," +
                                             "'" + (data["pstatus"]) + "' TYPE," +
                                             "'" + (data["pfaculty"]) + "' FACULTY," +
                                             "'" + (data["pclass"]) + "' CLASS" +
                                             " FROM DUAL) val "
                 "ON ( P.PERSON_ID = " + (data["pid"]) + ") "
                 "WHEN MATCHED THEN UPDATE SET P.NAME = '" + (data["pname"]) + "', " +
                                                "P.SURNAME = '" + (data["psurname"]) + "', " +
                                                "P.TYPE = '" + (data["pstatus"]) + "', " +
                                                "P.FACULTY = '" + (data["pfaculty"]) + "', " +
                                                "P.CLASS = '" + (data["pclass"]) + "'" +
                 " WHEN NOT MATCHED THEN INSERT (PERSON_ID, NAME, SURNAME, TYPE, FACULTY, CLASS) "
                 "VALUES (val.PERSON_ID, val.NAME, val.SURNAME, val.TYPE, val.FACULTY, val.CLASS)")

    conn.execute("INSERT INTO LEND_HEAD (PERSON_ID, STAFF_ID, LEND_DATE, DETAIL, CREATE_DATE, UPDATE_DATE) "
                 "VALUES (:1, :2, TO_DATE(:3, 'yyyy-mm-dd'), :4, TO_DATE(:5, 'yyyy-mm-dd'), TO_DATE(:6, 'yyyy-mm-dd'))",
                 (data["pid"], data["sid"], data["ldate"], data["ldetail"], data["cdate"], data["udate"]))

    conn.execute("INSERT INTO LEND_DETAIL (LEND_NO, EQUIPMENT_ID, CREATE_DATE, UPDATE_DATE) "
                 "SELECT MAX(LEND_NO)as LEND_NO, :3, TO_DATE(:4, 'yyyy-mm-dd'), TO_DATE(:5, 'yyyy-mm-dd') FROM LEND_HEAD",
                 (data["eid"], data["cdate"], data["udate"]))
    conn.commit()
    return json.dumps(data)

@app.route('/searchstu' , methods = ['POST' , 'GET'])
def searchstu():
    data = request.get_json()
    conn = db_connect.connect()
    query = conn.execute("SELECT NAME, SURNAME, TYPE, FACULTY, CLASS FROM PERSON WHERE PERSON_ID = " + (data["pid"]))
    rows = query.fetchall()

    for row in rows:
        list1 = ["NAME", "SURNAME", "TYPE", "FACULTY", "CLASS"]
        list2 = [row["name"], row["surname"], row["type"], row["faculty"], row["class"]]
        data = zip(list1, list2)
        d = dict(data)
        print(d)

    return jsonify(d)

@app.route('/report')
def report():
    return render_template("report.html")

@app.route('/getreport' , methods = ['POST'])
def getreport():

    datareport = request.form
    # print(json.loads(datareport[0])
    for i in range(len(datareport)):
        print(json.loads(datareport[str(i)]))


    return redirect(url_for('report'))

if __name__ == '__main__':
    app.run(debug=True)

