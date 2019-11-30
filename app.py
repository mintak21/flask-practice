# -*- coding: utf-8 -*-
import json
import sqlite3
import os


from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!!'


@app.route('/prime', methods=['GET'])
def handle_get():
    target = request.args.get('number')
    if not target:
        return 'number Parameterがたりん！！'
    result = target + 'は素数です。' if _isPrime(target) else target + 'は素数じゃないよ。'
    return render_template('prime.html', title='Prime Divider', result=result)


@app.route('/profile')
def profile():
    prof_dict = _get_all_profile_from_database()
    print('Users->', prof_dict)
    return render_template(
        'profile.html',
        title='User Profile',
        user_dict=prof_dict)


@app.route('/edit')
def edit():
    user_source = _get_profile()
    target_user_id = request.args.get('user_id')
    target_user = user_source.get(target_user_id)
    return render_template(
        'edit.html',
        title='User Edit Page',
        user_id=target_user_id,
        user=target_user)


@app.route('/update', methods=['POST'])
def update():
    user_source = _get_profile()

    user_id = request.form['key']
    target_user = user_source[user_id]
    # prof_dictの値を変更(updateなので、ここで新規は考えない)
    target_user['name'] = request.form['name']
    target_user['age'] = request.form['age']
    target_user['sex'] = request.form['sex']

    _update_profile(user_source)

    return redirect(url_for("profile"))


@app.route('/dot-pro')
def hive():
    return render_template('index.html', message='d')


@app.route('/var')
def var():
    return render_template('var.html', message='a')


@app.route('/fizzbuzz')
def handle_fizzbuzz():
    end = 100
    numbers = list()
    for num in range(1, end + 1):
        numbers.append(_fizzbuzz(num))
    result = '<br>'.join(numbers)
    return render_template('fizzbuzz.html', fizzbuzz_result=result)


def _get_profile():
    # JSONファイルの読み込み
    file_json = "data/profile.json"
    prof = open(file_json, encoding='utf-8')
    json_str = prof.read()
    prof.close()

    # JSONから辞書型に変換
    return json.loads(json_str)


def _get_all_profile_from_database():
    conn = None
    try:
        conn = sqlite3.connect('profile.sqlite3')
        c = conn.cursor()
        prof_list = dict()
        for i in c.execute('select * from persons'):
            prof_list[i[0]] = {'name': i[1], 'age': i[2], 'sex': i[3]}
        return prof_list
    finally:
        if not conn:
            conn.close()


def _update_profile_database(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('update persons set name=?,age=?,sex=? WHERE id= 1',
              (prof['name'], prof['age'], prof['sex']))
    conn.commit()
    conn.close()


def _update_profile(prof):
    f = open('data/profile.json', 'w')
    json.dump(prof, f)
    f.close()


def _fizzbuzz(num):
    if num % 15 == 0:
        return 'FizzBuzz'
    elif num % 3 == 0:
        return 'Fizz'
    elif num % 5 == 0:
        return 'Buzz'
    else:
        return str(num)


def _isPrime(num):
    try:
        int_num = int(num)
        if int_num == 1:
            return False
        for p in range(2, int_num):
            if int_num % p == 0:
                return False
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    print('Current Path is', os.getcwd())
    app.run(debug=True, port=9070)
