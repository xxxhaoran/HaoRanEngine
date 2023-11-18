from flask import Flask
from flask import render_template
from flask import request
from flask import session
from pymongo import MongoClient
from flask import Blueprint
from flask import redirect
import re
import hashlib
import time

admin_bp = Blueprint('admin', __name__, template_folder='templates')
client = MongoClient(host='127.0.0.1', port=27017)
collection = client['hao_ranWeb']['users']
app = Flask(__name__)
app.secret_key = 'THISISASTRONGKEY'
allowed_characters = r'^[a-zA-Z0-9_]+$'
login_attempts = {}

@app.route('/')
def index():
    if session:
        return render_template('index.html', username=session['username'])
    else:
        return render_template('index.html', username='尊敬的用户')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        userinfo = collection.find_one({'username': session['username']})
        return render_template('person.html', userinfo=userinfo)

    if request.method == 'POST':
        data = request.get_json()
        username = data['user']
        password = data['pass']
        if username == '':
            return {'message': '用户名为空!'}

        # 检查用户名字符是否合法
        allowed_characters = r'^[a-zA-Z0-9_]+$'
        if not re.match(allowed_characters, username):
            return {'message': '用户名只允许输入大小写字母与数字、下划线!'}

        # 检查账户是否已被锁定
        if username in login_attempts and login_attempts[username]['attempts'] >= 3:
            # 获取当前时间
            current_time = time.time()
            # 检查锁定截止时间是否已到达或过期
            if current_time <= login_attempts[username]['lock_time']:
                remaining_time = int(login_attempts[username]['lock_time'] - current_time)
                return {'message': f'该账户已被锁定，请在{remaining_time}秒后再尝试登录！'}

            # 若锁定时间已到达或过期，则解锁账户
            del login_attempts[username]

        res = collection.find_one({'username': username})
        if res is None or res['password'] != hashlib.md5(password.encode()).hexdigest():
            # 记录登录失败次数
            if username in login_attempts:
                login_attempts[username]['attempts'] += 1
            else:
                login_attempts[username] = {'attempts': 1}

            # 若登录次数超过3次，则锁定账户10分钟
            if login_attempts[username]['attempts'] >= 3:
                login_attempts[username]['lock_time'] = time.time() + 600

            return {'message': '用户名或密码错误!'}

        session['username'] = username
        return {'message': '登录成功!'}

    return render_template('login.html', name='login')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['user']
    password = data['input']
    check = data['input1']
    if username == '':
        return {'message': '用户名为空!'}
    if not re.match(allowed_characters, username):
        return {'message': '用户名只允许输入大小写字母与数字、下划线!'}
    if len(password) < 6:
        return {'message': '密码长度小于6位'}
    if check != password:
        return {'message': '密码不相同!'}
    if collection.find_one({'username':username}):
        return {'message': ' 账号已存在'}
    encodePass = hashlib.md5(check.encode())
    res = collection.insert_one(
        {
            'username': username, 'password': encodePass.hexdigest(),
            'address':'', 'phone':'',
            'gender':'', 'age':'',
            'flag':'1'
        })
    print(res)

    return {'message': '注册成功!'}


@app.route('/person')
def person():
    if session:
        userinfo = collection.find_one({'username': session['username']})
        return render_template('person.html', userinfo=userinfo)
    return 'Hacker!'

@app.route('/logout')
def logout():
    del session['username']
    return render_template('login.html', name='login')

'''
username: username,
gender: gender,
age: age,
address: address,
phone: phone
'''
@app.route('/changeinfo', methods=['POST'])
def changeInfo():
    data = request.json
    # print(data)
    username = data['username']
    gender = data['gender']
    address = data['address']
    phone = data['phone']
    age = data['age']
    res = collection.find_one({'username': username})
    if not res:
        return {"message": '没有此用户?Hacker!'}
    collection.update_one({'username': username}, {"$set": {
        'gender': gender,
        'address': address,
        'phone': phone,
        'age': age
    }})
    return {'message': '修改成功'}

@app.route('/changePassword',methods=['POST'])
def changePassword():
    data = request.form
    username = data['user']
    old_pass = data['pass0'] #旧密码
    new_pass = data['pass1'] #新密码
    check = data['pass2'] #新密码确认
    res = collection.find_one({'username': username})
    if not res:
        return {'message':'用户不存在'}
    if new_pass!=check:
        return {'message':'新密码不一致!'}
    old_pass = hashlib.md5(old_pass).hexdigest()
    new_pass = hashlib.md5(new_pass).hexdigest()
    if res['password']!=old_pass:
        return {'message':'旧密码错误!'}
    collection.update_one({"username": username},{"$set": {"password": new_pass}},False)


@admin_bp.route('/admin/', methods=['GET'])
def admin():
    if not session:
        return redirect('/login')
    # 查询所有用户信息的逻辑处理（示例）
    data = collection.find()
    res = collection.find_one({'username': session['username']})
    if res['flag'] != '0':
        return 'not permission!'

    return render_template('admin.html', users=data)


app.register_blueprint(admin_bp)


@app.route('/admin/delete/<username>')
def delete(username):
    collection.find_one_and_delete({'username':username})
    return redirect('/admin')

@app.route('/admin/add', methods=['POST'])
def add():
    data = request.form
    username = data['username']
    password = data['password']
    address = data['address']
    age = data['age']
    gender = data['gender']
    flag = data['flag']
    phone = data['phone']

    if username == '':
        return '用户名为空!'
    if not re.match(allowed_characters, username):
        return '用户名只允许输入大小写字母与数字、下划线!'
    if len(password) < 6:
        return '密码长度小于6位'
    if collection.find_one({'username': username}):
        return '账号已存在'
    encodePass = hashlib.md5(password.encode())
    res = collection.insert_one(
        {
            'username': username, 'password': encodePass.hexdigest(),
            'address': address, 'phone': phone,
            'gender': gender, 'age': age,
            'flag': flag
        })
    print(res)

    return redirect('/admin')

@app.route('/admin/edit/<username>')
def edit(username):
    user = collection.find_one({'username':username})
    return render_template('edit.html', user=user)

'''
username: username,
gender: gender,
age: age,
address: address,
phone: phone
'''
@app.route('/admin/update/<username>',methods=['POST'])
def update(username):
    data = request.form
    username = data['username']
    password = data['password']
    gender = data['gender']
    age = data['age']
    address = data['address']
    phone = data['phone']
    flag = data['flag']
    check = collection.find_one({'username':username})['password']
    if check != password:
        password == hashlib.md5(password.encode()).hexdigest()
    collection.find_one_and_update({'username': username}, {"$set":{
        'username': username, 'password': password,
        'address': address, 'phone': phone,
        'gender': gender, 'age': age,
        'flag': flag
    }})
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)