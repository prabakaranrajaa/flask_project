from flask import Flask,render_template,url_for,redirect,request,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#my sql connection
app.config["MYSQL_HOST"]= "localhost"
app.config["MYSQL_USER"]= "root"
app.config["MYSQL_PASSWORD"]= "admin"
app.config["MYSQL_DB"]= "crud"
app.config["MYSQL_CURSORCLASS"]= "DictCursor"
mysql=MySQL(app)


#Loading home page
@app.route('/')
def home():
    con= mysql.connection.cursor()
    sql="select * from users"
    con.execute(sql)
    res=con.fetchall()
    return render_template("home.html",datas=res)


# new user insert
@app.route('/addusers', methods=['GET','POST'])
def addusers():
    if request.method=="POST":
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        con= mysql.connection.cursor()
        sql="insert into users (NAME,CITY,AGE) values(%s,%s,%s)"
        con.execute(sql,[name,city,age])
        mysql.connection.commit()
        con.close()
        flash("User Added Succesfully")
        return redirect(url_for("home"))
    return render_template("addUsers.html")

#update users
@app.route('/updateuser/<string:id>', methods=['GET','POST'])
def updateuser(id):
    con= mysql.connection.cursor()
    if request.method=="POST":
        name=request.form['name']
        city=request.form['city']
        age=request.form['age']
        sql="update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql,[name,city,age,id])
        mysql.connection.commit()
        con.close()
        flash("User Updated Succesfully")
        return redirect(url_for("home"))
    sql="select * from users where ID=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("updateUser.html",datas=res)

#delete user
@app.route('/deleteuser/<string:id>', methods=['GET','POST'])
def deleteuser(id):
    con= mysql.connection.cursor()
    sql="delete from users where ID=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash("User Deleted Succesfully")
    return redirect(url_for("home"))


if __name__=='__main__':
    app.secret_key="abc123"
    app.run(debug=True)