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
            "SELECT id, username, password, role FROM users WHERE email=%s",  #fikk hjelp fra ki
            (email,)
        )
        user = cursor.fetchone()
        mydb.close()

        if user and user[2] == passord:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            flash("Innlogget!")
            if user[3] == "admin":  #fikk hjelp fra ki med dette
                return redirect("/admin")
            else:
                return redirect("/book")
        
        flash("Feil email eller passord")

    return render_template("login.html")

@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return redirect("/login")
    
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT appointment.id, users.username, service.name, appointment.date, appointment.time FROM appointment JOIN users ON appointment.user_id = users.id JOIN service ON appointment.service_id = service.id"
    )
    bookings = cursor.fetchall()
    mydb.close()
    return render_template("admin.html", bookings=bookings)

@app.route("/admin/edit/<int:cid>")
def edit_booking(cid):
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT id, date, time FROM appointment WHERE id = %s", (cid,))
    appointment = cursor.fetchone()
    cursor.close()
    mydb.close()
    return render_template("edit_booking.html", appointment=appointment)



@app.route("/admin/update", methods=["POST"])
def update_booking():
    bid = request.form["id"]
    date = request.form["date"]
    time = request.form["time"]
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("UPDATE appointment SET date = %s, time = %s WHERE id = %s", (date, time, bid))
    mydb.commit()
    cursor.close()
    return redirect("/admin")

@app.route("/admin/delete/<int:cid>")
def delete_booking(cid):
    mydb = get_connection()
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM appointment WHERE id = %s", (cid,))
    mydb.commit()
    cursor.close()
    mydb.close()
    return redirect("/admin")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

            
if __name__ == "__main__":
    app.run(debug=True)
