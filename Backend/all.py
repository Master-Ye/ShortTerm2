
from datetime import datetime
import mysql.connector
from flask import Flask, request, send_file, Response, make_response, jsonify
from flask_cors import cross_origin
import jwt
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="jiweijian",
  database="runoob",
    buffered=True
)
app = Flask(__name__)
def generate_token(payload):
    # 定义 payload，包含需要在 Token 中携带的数据


    # 定义密钥
    secret_key = 'ruanjiankaifashijian'  # 替换为你自己的密钥，请保密

    # 生成 Token
    token = jwt.encode(payload, secret_key, algorithm='HS256')

    # 将生成的 Token 返回
    return token



@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    username = data['username']
    password = data['password']
    cursor = db.cursor()
    query = "SELECT * FROM user WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    if result:
        # 登录成功，取出 class 值
        user_class = result[3]
        temp={
            'username':username,
            'password':password,
        }
        t={
            'code':200,
            'class':user_class,
            'username':username,
            'password':password,
            'token':generate_token(temp),
            'msg':"success"

        }
        return t
    else:
        # 登录失败
        t={
            'code':400,
            'msg':'登录失败'

        }
        return t
    # 获取查询结果
    result = cursor.fetchone()
@app.route('/reason', methods=['get'])
@cross_origin()
def reason():

    cursor = db.cursor()
    sql = "select * from   reason "

    cursor.execute(sql)

    # 获取查询结果
    result = cursor.fetchall()

    # 获取表的字段信息
    columns = [desc[0] for desc in cursor.description]

    # 将查询结果转换为字典列表
    records_dict = [dict(zip(columns, row)) for row in result]


    # 返回JSON响应
    return jsonify(records_dict)

@app.route('/reason2', methods=['get'])
@cross_origin()
def reason2():

    cursor = db.cursor()
    sql = "select * from   rereason "

    cursor.execute(sql)

    # 获取查询结果
    result = cursor.fetchall()

    # 获取表的字段信息
    columns = [desc[0] for desc in cursor.description]

    # 将查询结果转换为字典列表
    records_dict = [dict(zip(columns, row)) for row in result]


    # 返回JSON响应
    return jsonify(records_dict)

@app.route('/application', methods=['post'])
@cross_origin()
def application():
    data = request.form
    file = request.files['file']
    file_data = file.read()
    # 提取参数

    c_or_w = int(data['c_or_w'])
    check_t = data['check_t']
    s = int(data['s'])
    severe = data['severe']
    app_time = data['app_time']
    app_acc = data['app_acc']
    check_acc = data['check_acc']
    reason_id = int(data['reason_id'])
    cus_id = data['cus_id']
    print(cus_id)
    app_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    cursor = db.cursor()
    sql = """
               INSERT INTO application ( c_or_w,  file, s, severe, app_time, app_acc, check_acc, reason_id, cus_id)
             VALUES ( %s, %s,  %s, %s, NOW(), %s, %s, %s, %s)
           """

    cursor.execute(sql,(c_or_w,file_data,s,severe,app_acc,check_acc,reason_id,cus_id))

    # 获取查询结果

    db.commit()
    t={
        'res':200
    }
    # 返回JSON响应
    return t

@app.route('/updatereason', methods=['POST'])
@cross_origin()
def updatereason():
    data = request.json
    cursor = db.cursor()
    for obj in data:
        on1 = obj['on1']
        reason_id = obj['reason_id']

        # 更新数据库中的数据

        cursor.execute("UPDATE reason SET on1 = %s WHERE reason_id = %s", (on1, reason_id))
        db.commit()


    return 'Data updated successfully'
@app.route('/aud2list', methods=['get'])
@cross_origin()
def aud2list():

    cursor = db.cursor()
    sql = """
               SELECT beizhu,cus_id,cname,outLevel,reason_id,severe,check_acc,app_time,rereasonid,s,c_or_w FROM customer natural JOIN application natural  join company
           """

    cursor.execute(sql)
    data = cursor.fetchall()
    # 获取查询结果

    columns = [desc[0] for desc in cursor.description]

    # 将查询结果转换为字典列表
    records_dict = [dict(zip(columns, row)) for row in data]

    # 返回JSON响应
    return jsonify(records_dict)

@app.route('/pdf', methods=['post'])
@cross_origin()
def pdf():

    id = request.form['id']
    # 获取查询结果
    cursor = db.cursor()

    sql = """
                   SELECT file FROM customer natural JOIN application where cus_id=%s
               """
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    pdf_data = result[0]
    print(pdf_data)
    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=your_filename.pdf'

    return response


@app.route('/application1', methods=['post'])
@cross_origin()
def application1():
    data = request.form

    # 提取参数

    c_or_w = int(data['c_or_w'])

    s = int(data['s'])
    severe = data['severe']

    app_acc = data['app_acc']
    check_acc = data['check_acc']
    reason_id = int(data['reason_id'])
    cus_id = data['cus_id']
    print(cus_id,"aaa")

    cursor = db.cursor()
    sql = """
               INSERT INTO application ( c_or_w,  s, severe, app_time, app_acc, check_acc, rereasonid
               , cus_id)
             VALUES ( %s, %s,  %s,  NOW(), %s, %s, %s, %s)
           """

    cursor.execute(sql,(c_or_w,s,severe,app_acc,check_acc,reason_id,cus_id))

    # 获取查询结果

    db.commit()
    t={
        'res':200
    }
    # 返回JSON响应
    return t

@app.route('/data', methods=['GET'])
@cross_origin()
def get_data():
    cursor = db.cursor()

    cursor.execute("SELECT *   FROM customer natural JOIN company ")
    data = cursor.fetchall()
    print(data)
    columns = [desc[0] for desc in cursor.description]

    # 将查询结果转换为字典列表
    records_dict = [dict(zip(columns, row)) for row in data]

    # 返回JSON响应
    return jsonify(records_dict)


@app.route('/viewdata', methods=['GET'])
@cross_origin()
def viewdata():
    cursor = db.cursor()

    cursor.execute("SELECT *   FROM customer natural JOIN company")
    data = cursor.fetchall()
    print(data)
    columns = [desc[0] for desc in cursor.description]

    # 将查询结果转换为字典列表
    records_dict = [dict(zip(columns, row)) for row in data]

    # 返回JSON响应
    return jsonify(records_dict)


@app.route('/agreere', methods=['POST'])
@cross_origin()
def agreere():
    cursor = db.cursor()
    data = request.json
    id = data.get('cus_id')
    name = data.get('name')

    print(id)
    sql = """
               UPDATE customer SET ss = 0 WHERE cus_id = %s and ss=1
               """
    current_time = datetime.utcnow()
    cursor.execute(sql, (id,))
    db.commit()
    sql = """
                   UPDATE application SET s = 1,check_t=NOW(),check_acc=%s WHERE cus_id = %s and c_or_w=1 
                   """

    cursor.execute(sql, (name,id))
    t={
        'code':200
    }
    # 返回JSON响应
    return t
@app.route('/disagreere', methods=['POST'])
@cross_origin()
def disagreere():
    cursor = db.cursor()
    data = request.json
    id = data.get('cus_id')
    name = data.get('name')

    print(id,name)
    current_time = datetime.utcnow()


    sql = """
                   UPDATE application SET s = 2,check_t=NOW(),check_acc=%s WHERE cus_id = %s and c_or_w=1 and s=0
                   """

    cursor.execute(sql, (name,id))
    t={
        'code':200
    }
    # 返回JSON响应
    return t




@app.route('/data1', methods=['GET'])
@cross_origin()
def get_data1():
    cursor = db.cursor()

    cursor.execute("SELECT cus_id,cname,reason_id,app_time,check_acc,check_t,outLevel  FROM customer  natural JOIN application where s=1 and c_or_w=0 ")
    data = cursor.fetchall()
    print(data)
    columns = [desc[0] for desc in cursor.description]

    # 将查询结果转换为字典列表
    records_dict = [dict(zip(columns, row)) for row in data]

    # 返回JSON响应
    return jsonify(records_dict)




@app.route('/agreede', methods=['POST'])
@cross_origin()
def agreede():
    cursor = db.cursor()
    data = request.json
    id = data.get('cus_id')
    name = data.get('name')

    print(id)
    sql = """
               UPDATE customer SET ss = 1 WHERE cus_id = %s
               """
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    cursor.execute(sql, (id,))
    db.commit()
    sql = """
                   UPDATE application SET s = 1,check_t=NOW(),check_acc=%s WHERE cus_id = %s and c_or_w=0 and s=0 
                   """

    cursor.execute(sql, (name,id))
    t={
        'code':200
    }
    # 返回JSON响应
    return t

@app.route('/disagreede', methods=['POST'])
@cross_origin()
def disagreede():
    cursor = db.cursor()
    data = request.json
    id = data.get('cus_id')
    name = data.get('name')

    print(id,name)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')


    sql = """
                   UPDATE application SET s = 2,check_t=NOW(),check_acc=%s WHERE cus_id = %s and c_or_w=0 and s=0
                   """

    cursor.execute(sql, (name,id))
    t={
        'code':200
    }
    # 返回JSON响应
    return t

@app.route('/reallist', methods=['get'])
@cross_origin()
def reallist():
    cursor = db.cursor()
    sql = """
                   SELECT cname,outLevel,reason_id,severe,check_t,check_acc,app_time,s FROM customer natural JOIN application where c_or_w=0
               """

    cursor.execute(sql)
    data = cursor.fetchall()
    # 获取查询结果

    columns = [desc[0] for desc in cursor.description]

    # 将查询结果转换为字典列表
    records_dict = [dict(zip(columns, row)) for row in data]

    # 返回JSON响应
    return jsonify(records_dict)





if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)