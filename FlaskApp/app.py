from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wit import Wit
import logging

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Akila  92'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')
    # return "Welcome!"

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    # validate the received values
    if _name and _email and _password:

        # All Good, let's call MySQL
        conn = mysql.connect()
        cur = conn.cursor()
        # _hashed_password = generate_password_hash(_password)
        cur.callproc('sp_createUser', (_name, _email, _password))
        data = cur.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})

        cur.close()
        conn.close()

    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})


@app.route('/witTest')
def WitTest():
    token = '7F63TXDBHOOOTQZ52MM5PALSEWPMXA6F'
    client = Wit(token)
    client.logger.setLevel(logging.DEBUG)
    print("Hello1")
    resp = client.message('I need more info about flex')
    print("Hello2")
    return ('Yay, got Wit.ai response: ' + str(resp))



if __name__ == "__main__":
    app.run()
