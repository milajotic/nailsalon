from flask import Flask, render_template, request, redirect, session, flash
from db import get_connection
import os
import mariadb
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "temp-secret")


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)  #last .env fila
env_User = os.getenv("DB_USER")
env_Host = os.getenv("DB_HOST")
env_Password = os.getenv("DB_PASSWORD")
env_Database = os.getenv("DB_NAME")

def get_connection():
    return mariadb.connect(
        host = env_Host,
        user = env_User,
        password = env_Password,
        database = env_Database
    )



@app.route("/")
def index():
    return render_template("index.html")



@app.route("/services", methods=["GET", "POST"])
def services_side():
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    mydb.close()
    return render_template("services.html", services=services)



@app.route("/book", methods=["GET", "POST"])
def login_registrer():
    if "user_id" not in session:
        flash("Du må logge inn for å bestille time")
        return redirect("/login")
    
    mydb = get_connection()
    cursor = mydb.cursor()

    if request.method == "POST":
        service_id = request.form["service"]
        date = request.form["dato"]
        time = request.form["tid"]

        cursor.execute(
            "INSERT INTO appointment (user_id, service_id, date, time) VALUES (%s,%s,%s,%s)",
            (session["user_id"], service_id, date, time)
        )
        mydb.commit()

        flash("Tusen takk for bestillingen! Vi gleder oss til å se deg <3")
        return redirect("/book")
    

    cursor.execute("SELECT * FROM service")
    services = cursor.fetchall()
    mydb.close()

    return render_template("book.html", services=services)




@app.route("/registrer", methods=["GET", "POST"])
def book_side():
    mydb = get_connection()
    cursor = mydb.cursor()

    if request.method == "POST":
        navn = request.form["navn"]
        email = request.form["email"]
        passord = request.form["password"]

        mydb = get_connection()
        cursor = mydb.cursor()

        cursor.execute(
            "Select id FROM users WHERE email=%s",
            (email,)
        )
        existing = cursor.fetchone()

        if existing:
            flash("Email finnes allerede. Logg inn i stedet.")
            return redirect ("/login")
        
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s,%s,%s)",
            (navn, email, passord)
        )
        mydb.commit()

        session["user_id"] = cursor.lastrowid
        session["username"]= navn

        flash ("Bruker opprettet! Du er nå innlogget.")
        return redirect("/book")
    

    return render_template("registrer.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        passord = request.form["password"]

        mydb = get_connection()
        cursor = mydb.cursor()

        cursor.execute(
            "SELECT id, username, password FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()
        mydb.close()

        if user and user [2] == passord:
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash("Feil email eller passord")
            return redirect("/book")
        
        flash("Feil email eller passord")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

            




if __name__ == "__main__":
    app.run(debug=True)
