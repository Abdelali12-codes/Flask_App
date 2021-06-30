from flask import Flask
from flask import *

import sqlite3
app = Flask(__name__)  # creating the Flask class object


@app.route('/')  # decorator drfines the
def index():
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def login():
    uname = request.form['uname']
    passwrd = request.form['pass']

    if uname == "abdelali" and passwrd == "google":
        return "Welcomne %s" % uname


@app.route('/name/<name>')
def name(name):
    return "Hello , "+name


@app.route("/delimiter/<uname>")
def delimiter(uname):

    if uname == "abdelali":
        return render_template("home.html", name=uname)
    else:
        return 'Error that was not the name that is expected'


@app.route("/table/<int:num>")
def table(num):
    return render_template("multiplication.html", n=num)


@app.route("/customer")
def customer():
    return render_template("customer.html")


@app.route("/success", methods=["POST", "GET"])
def success():
    if request.method == "POST":
        result = request.form
        return render_template("result_data.html", result=result)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form['name']
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT into Employees(name ,email , address) values(? , ? ,?) ", (name, email, address))

                con.commit()
                msg = "Employee succefully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)


@app.route("/view")
def view():
    con = sqlite3.connect("employee.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()

    return render_template("view.html", rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
