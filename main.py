import datetime
import re
from flask import Flask, render_template, request, jsonify, flash, redirect
from database import accessData

app = Flask(__name__)
app.secret_key = "secret"

handler = accessData()


# ----------------------------SearchUI-------------------------------------------
@app.route('/')
def searchUI():
    return render_template('searchUI.html')


#  search in database
@app.route("/search", methods=['POST'])
def listSearch():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    mobile_no = request.form["mobile_no"]

    query = "select * from users where "
    if first_name != "":
        query += f"first_name='{first_name}' "

    if last_name != "":
        if first_name != "":
            query += f" and last_name='{last_name}' "
        else:
            query += f" last_name='{last_name}' "

    if mobile_no != "":
        if first_name != "" or last_name != "":
            query += f" and mobile_no='{mobile_no}' "
        else:
            query += f" mobile_no='{mobile_no}' "

    if first_name == "" and last_name == "" and mobile_no == "":
        query = "select * from users"
    data = handler.fetchData(query)
    return render_template('list.html', data=data, length=len(data))

# ----------create user ui---------------------

@app.route("/addRecords")
def adddata():
    return render_template('addRecords.html')


# add user in database
@app.route("/addUser", methods=['POST'])
def addUser():
    values = ()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['mobile_no']
        if len(first_name) <=3 :

            flash("First Name  must  contain  atleast  4 characters")
            return redirect('addRecords')
        else:
            values = (first_name,)

        if len(last_name) <=3:
            flash("Last Name  must  contain  atleast  4 characters")
            return redirect('addRecords')
        else:
            values=(last_name,)
        if len(first_name) and len(last_name) <=3:
            flash("First Name and Last Name  must  contain  atleast  4 characters")
            return redirect('addRecords')
        else:
            values=(first_name,last_name)

        # rule = re.compile(r'/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/')
        rule =re.compile(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$')
        if not rule.match(phone):
            flash("invalid Mobile Number")
            return redirect('addRecords')
        else:
            values = (first_name, last_name, phone, request.form["address"], str(datetime.datetime.now()))
    # print(values)
    # values = (request.form['first_name'], request.form['last_name'],
    #           request.form['mobile_no'], request.form["address"], str(datetime.datetime.utcnow()))
    handler.addData(values)
    flash("User Added Successfully")
    #     data=handler.fetchData('select * from users')
    return redirect('addRecords')


# --------------------Display All The List Of Data-----------------

@app.route("/list")
def showlist():
    querry = "select * from users"
    data = handler.fetchData(querry)
    return render_template('list.html', data=data, length=len(data))


@app.route("/API")
def showAPI():
    return jsonify(handler.fetchData('select * from users'))


# ------------------------------Delete The Row From Database----------------------

@app.route("/delete")
def deleteData():
    id = request.args.get('id')
    querry = f'delete from users where id={id}'
    handler.delete(querry)
    data = (handler.fetchData('select * from users'))
    flash("User Deleted Successfully")
    return render_template('list.html', data=data, length=len(data))


# -----------------------------------Update UI---------------------------------------

@app.route("/update")
def updatedData():
    id = request.args.get('id')
    data = handler.getData(id)
    return render_template('updateUI.html', data=data[0])


# ---------------------Update Data in Database-----------------------

@app.route("/updateUser", methods=['POST'])
def updateData():

    values = (request.form['first_name'], request.form['last_name'], request.form['mobile_no'], request.form["address"])
    handler.updateData(values, request.form['ID'])
    flash("User Details Updated Successfully")
    return redirect('list')


# ----------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
