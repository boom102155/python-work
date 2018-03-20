from flask import Flask, jsonify, render_template, request, json, redirect, url_for, session
from sqlalchemy import create_engine
from time import gmtime, strftime
import datetime
import os


os.environ["NLS_LANG"] = ".UTF8"
db_connect = create_engine('oracle://ADBOOM:boom125478@127.0.0.1:1521/xe')

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.secret_key = os.urandom(24)
datareport = {}

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/loginsubmit' , methods = ['POST' , 'GET'])
def loginsubmit():
    data = request.get_json()
    conn = db_connect.connect()
    query = conn.execute("SELECT USER_NAME FROM STAFF "
                         "WHERE USER_NAME = '" + (data["user"]) + "'" +
                         " AND PASSWORD = '" + (data["pass"]) + "'")
    rows = query.fetchall()
    for row in rows:
        # list1 = ["NAME", "SURNAME"]
        # list2 = [row["name"], row["surname"]]
        list1 = ["USER_NAME"]
        list2 = [row["user_name"]]
        data = zip(list1, list2)
        d = dict(data)
        session['user'] = ''.join(list2)

    return jsonify(d)

@app.route('/profile' , methods = ['POST' , 'GET'])
def profile():
    conn = db_connect.connect()
    if 'user' in session:
        username = session['user']
        query1 = conn.execute("SELECT NAME, SURNAME, USER_NAME, PASSWORD FROM STAFF "
                              "WHERE USER_NAME = '" + username + "'")
        rows = query1.fetchall()
        for row in rows:
            list1 = ["NAME", "SURNAME", "user_name", "password"]
            list2 = [row["name"], row["surname"], row["user_name"], row["password"]]
            # data = zip(list1, list2)
            # d = dict(data)
            name = row["name"]
            surname = row["surname"]
            usn = row["user_name"]
            pw = row["password"]
            return render_template("profile.html", username=username, name=name, surname=surname, usn=usn, pw=pw)

    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

@app.route('/editpassword' , methods = ['POST' , 'GET'])
def editpassword():
    data = request.get_json()
    conn = db_connect.connect()
    username = session['user']
    conn.execute("UPDATE STAFF SET PASSWORD = '" + (data["confirmpw"]) + "' WHERE USER_NAME = '" + username + "'")
    conn.commit()
    return json.dumps(data)

@app.route('/index')
def index():
    if 'user' in session:
        return render_template("index.html")
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return 'Dropped'

@app.route('/person')
def person():
    conn = db_connect.connect()
    query = conn.execute("SELECT PERSON_ID, (NAME || ' ' || SURNAME) as n, TYPE, FACULTY, CLASS FROM PERSON")
    rows = query.fetchall()
    if 'user' in session:
        username = session['user']
        return render_template("person.html", rows=rows, username=username)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

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

    query2 = conn.execute("SELECT EQUIPMENT_ID, EQUIPMENT_NAME FROM EQUIPMENT ORDER BY EQUIPMENT_NAME ASC")
    rows2 = query2.fetchall()

    pidautocomplete = conn.execute("SELECT PERSON_ID FROM PERSON")
    rows3 = pidautocomplete.fetchall()

    if 'user' in session:
        username = session['user']
        query3 = conn.execute("SELECT STAFF_ID FROM STAFF "
                              "WHERE USER_NAME = '" + username + "'")
        rows = query3.fetchall()
        for row in rows:
            list1 = ["STAFF_ID"]
            list2 = [row["staff_id"]]
            # data = zip(list1, list2)
            # d = dict(data)
            staffid = ', '.join(str(x) for x in list2)
        return render_template("lend.html", rows1=rows1, rows2=rows2, rows3=rows3, username=username, staffid=staffid)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"


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

    if 'user' in session:
        username = session['user']
        return render_template("equipment.html", rows1=rows1 , rows2=rows2 , rows3=rows3, username=username)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
      "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

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

    if 'user' in session:
        username = session['user']
        return render_template("category.html", rows=rows, username=username)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

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

@app.route('/report' , methods = ['POST' , 'GET'])
def report():
    result = request.form
    d = result["json"]
    # d = json.loads(result["json"])
    print(d)
    return render_template("report.html")

@app.route('/getreport' , methods = ['POST' , 'GET'])
def getreport():

    datareport = request.form
    # print(json.loads(datareport[0])
    for i in range(len(datareport)):
        print(json.loads(datareport[str(i)]))

    return redirect(url_for('report'))


# ==================Room Checker===================

@app.route('/room' , methods = ['POST' , 'GET'])
def room():
    conn = db_connect.connect()
    if 'user' in session:
        username = session['user']
        query = conn.execute("SELECT STAFF_ID FROM STAFF "
                             "WHERE USER_NAME = '" + username + "'")
        rows = query.fetchall()
        for row in rows:
            list1 = ["STAFF_ID"]
            list2 = [row["staff_id"]]
            # data = zip(list1, list2)
            # d = dict(data)
            staffid = ', '.join(str(x) for x in list2)
            return render_template("room.html", username=username, staffid=staffid)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

# ================= 941 ===================
@app.route('/room941' , methods = ['POST' , 'GET'])
def room941():
    conn = db_connect.connect()
    if 'user' in session:
        username = session['user']
        query = conn.execute("SELECT STAFF_ID FROM STAFF "
                              "WHERE USER_NAME = '" + username + "'")
        rows = query.fetchall()
        for row in rows:
            list1 = ["STAFF_ID"]
            list2 = [row["staff_id"]]
            # data = zip(list1, list2)
            # d = dict(data)
            staffid = ', '.join(str(x) for x in list2)
            return render_template("941.html", username=username, staffid=staffid)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

# ================= 953 ===================
@app.route('/room953' , methods = ['POST' , 'GET'])
def room953():
    conn = db_connect.connect()
    if 'user' in session:
        username = session['user']
        query = conn.execute("SELECT STAFF_ID FROM STAFF "
                             "WHERE USER_NAME = '" + username + "'")
        rows = query.fetchall()
        for row in rows:
            list1 = ["STAFF_ID"]
            list2 = [row["staff_id"]]
            # data = zip(list1, list2)
            # d = dict(data)
            staffid = ', '.join(str(x) for x in list2)
            return render_template("953.html", username=username, staffid=staffid)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

# ================= 982 ===================
@app.route('/room982' , methods = ['POST' , 'GET'])
def room982():
    conn = db_connect.connect()
    if 'user' in session:
        username = session['user']
        query = conn.execute("SELECT STAFF_ID FROM STAFF "
                             "WHERE USER_NAME = '" + username + "'")
        rows = query.fetchall()
        for row in rows:
            list1 = ["STAFF_ID"]
            list2 = [row["staff_id"]]
            # data = zip(list1, list2)
            # d = dict(data)
            staffid = ', '.join(str(x) for x in list2)
            return render_template("982.html", username=username, staffid=staffid)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

# ================= 983 ===================
@app.route('/room983' , methods = ['POST' , 'GET'])
def room983():
    conn = db_connect.connect()
    if 'user' in session:
        username = session['user']
        query = conn.execute("SELECT STAFF_ID FROM STAFF "
                             "WHERE USER_NAME = '" + username + "'")
        rows = query.fetchall()
        for row in rows:
            list1 = ["STAFF_ID"]
            list2 = [row["staff_id"]]
            # data = zip(list1, list2)
            # d = dict(data)
            staffid = ', '.join(str(x) for x in list2)
            return render_template("983.html", username=username, staffid=staffid)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

# ================= checklist ===================
@app.route('/roomchecklist' , methods = ['POST' , 'GET'])
def roomchecklist():
    conn = db_connect.connect()
    if 'user' in session:
        username = session['user']
        query1 = conn.execute("SELECT ID, rc.ROOM_NAME, rc.LOCATION, rc.STATUS, rc.DESCRIPTION, (s.NAME || ' ' || s.SURNAME) AS staff, TO_CHAR(rc.CHECK_DATE,'yyyy-mm-dd') AS checkdate "
                              "FROM ROOM_CHECKER rc , STAFF s "
                              "WHERE rc.STAFF_ID = s.STAFF_ID")
        query2 = conn.execute("SELECT STAFF_ID FROM STAFF "
                             "WHERE USER_NAME = '" + username + "'")
        rows1 = query1.fetchall()
        rows2 = query2.fetchall()
        for row in rows2:
            list1 = ["STAFF_ID"]
            list2 = [row["staff_id"]]
            # data = zip(list1, list2)
            # d = dict(data)
            staffid = ', '.join(str(x) for x in list2)
            return render_template("room-check-list.html", username=username, staffid=staffid, rows1=rows1)
    return "คุณยังไม่ได้ลงชื่อเข้าใช้งานระบบ <a href = '/login'></b>" + \
           "คลิกที่นี่เพื่อลงชื่อเข้าใช้งาน</b></a>"

@app.route('/saveroom941' , methods = ['POST' , 'GET'])
def saveroom941():
    data = request.get_json()
    conn = db_connect.connect()
    conn.execute("INSERT INTO ROOM_CHECKER "
                     "(ROOM_NAME, "
                     "LOCATION, "
                     "STATUS, "
                     "DESCRIPTION, "
                     "STAFF_ID, "
                     "CHECK_DATE) "
                     "VALUES (:1, :2, :3, :4, :5, to_date(:6, 'yyyy-mm-dd'))",
                     (data["rname"], data["locate"], data["status"], data["description"], data["checker"], data["cdate"]))
    conn.commit()
    conn.rollback()
    return json.dumps(data)

@app.route('/preport' , methods = ['POST' , 'GET'])
def preport():
    conn = db_connect.connect()
    query1 = conn.execute("SELECT PERSON_ID, (NAME || ' ' || SURNAME) as perfessorname "
                          "FROM person "
                          "WHERE PERSON_ID BETWEEN 1001 and 1999")
    query2 = conn.execute("SELECT PERSON_ID, (NAME || ' ' || SURNAME) as perfessorname "
                          "FROM person "
                          "WHERE PERSON_ID BETWEEN 2001 and 2999")
    query3 = conn.execute("SELECT STAFF_ID, (NAME || ' ' || SURNAME) as staffname "
                          "FROM STAFF")
    query4 = conn.execute("SELECT d.DOC_ID, TO_CHAR(d.DOC_DATE,'yyyy-mm-dd') as docdate, d.DOC_NO, d.TOPIC, d.PATH_PIC, (p.NAME || ' ' || p.SURNAME) as person "
                          "FROM DOCUMENT d , PERSON_DOC pd , PERSON p "
                          "WHERE d.DOC_ID = pd.DOC_ID AND pd.PERSON_ID = p.PERSON_ID")

    rows1 = query1.fetchall()
    rows2 = query2.fetchall()
    rows3 = query3.fetchall()
    rows4 = query4.fetchall()

    return render_template("preport.html" , rows1=rows1 , rows2=rows2 , rows3=rows3, rows4=rows4)


@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      # f = request.files['file']
      # f.save(secure_filename(f.filename))
      # return 'file uploaded successfully'
      target = os.path.join(APP_ROOT, 'UPLOAD')
      print(target)
      file = request.files['file']
      if file.filename == '':
          return 'no file selected'

      if not os.path.isdir(target):
          os.mkdir(target)

      st = strftime("%d%m%Y", gmtime())
      t1 = strftime("%H", gmtime())
      t2 = strftime("%M", gmtime())
      t3 = strftime("%S", gmtime())

      for file in request.files.getlist("file"):
          print(file)
          filename = file.filename
          destination = "/".join([target, st + '_' + t1 + t2 + t3 + '.'+ filename.split('.')[1]])
          print("Accept incoming file:", filename.split('.')[1])
          print(destination)
          file.save(destination)
      return redirect("/preport")

@app.route('/adddocdata', methods = ['GET' , 'POST'])
def adddocdata():
    try:
        data = request.get_json()
        st = strftime("%d%m%Y", gmtime())
        t1 = strftime("%H", gmtime())
        t2 = strftime("%M", gmtime())
        t3 = strftime("%S", gmtime())

        constrname = st + '_' + t1 + t2 + t3 + '.' + (data['pathpic'])
        conn = db_connect.connect()
        conn.execute("INSERT INTO DOCUMENT "
                     "(DOC_DATE, "
                     "DOC_NO, "
                     "TOPIC, "
                     "PATH_PIC) "
                     "VALUES (TO_DATE(:1, 'yyyy-mm-dd'), :2, :3, :4)",
                     (data['docdate'], data['docnum'], data['docstory'], constrname))
        conn.commit()
    except:
        conn.rollback()
    finally:
        return json.dumps(data)
        conn.close()

@app.route('/addperson' , methods  = ['POST' , 'GET'])
def addperson():
    try:
        data = request.get_json()
        conn = db_connect.connect()
        conn.execute("INSERT INTO PERSON "
                     "(PERSON_ID, "
                     "NAME, "
                     "SURNAME, "
                     "TYPE, "
                     "FACULTY, "
                     "CLASS) "
                     "VALUES (:1, :2, :3, :4, :5, :6)",
                     (data["pid"], data["name"], data["sname"], data["type"], data["fac"], data["pclass"]))

        conn.commit()
    except:
        conn.rollback()
    finally:
        return json.dumps(data)
        conn.close()

@app.route('/testadd' , methods = ['POST' , 'GET'])
def testadd():
    data = request.get_json()
    # conn = db_connect.connect()
    # conn.execute()
    # conn.commit()
    print(data["getcheckdata"])
    return  json.dumps(data)

if __name__ == '__main__':
    app.run(debug=True)

