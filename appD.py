import os
from flask import (
    Flask,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
    flash,
    session,
)
from dataProcessing import *
from Threads import *
from flask import send_file
from werkzeug.utils import secure_filename
import sqlite3
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set your secret key

UPLOAD_FOLDER = "."
ALLOWED_EXTENSIONS = set(["txt"])

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CACHE_TYPE"] = "null"
app.static_folder = "static"


# Create a database connection
def create_connection():
    connection = sqlite3.connect("user.db")
    return connection


# Create a users table if it doesn't exist
def create_users_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """
    )
    connection.commit()
    connection.close()


# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = create_connection()
        cursor = connection.cursor()

        # Check if the username is already taken
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username is already taken", "error")
        else:
            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password),
            )
            connection.commit()
            flash("Registration successful", "success")
            return redirect(url_for("login"))

        connection.close()

    return render_template("register.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = create_connection()
        cursor = connection.cursor()

        # Check if the username and password match
        cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?", (username, password)
        )
        user = cursor.fetchone()

        if user:
            session["user_id"] = user[0]  # Store the user ID in the session
            flash("Login successful", "success")
            return redirect(
                url_for("indexD")
            )  # Redirect to index() after successful login
        else:
            flash("Login failed. Please check your credentials.", "error")

        connection.close()

    return render_template("login.html")


# Logout route
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main1"))  # Redirect to main() after logout


def resultD():
    return render_template("resultD.html")


@app.route("/decrypt/")
def DecryptMessage():
    st = time.time()
    HybridDeCrypt()
    et = time.time()
    print(et - st)
    trim()
    st = time.time()
    Merge()
    et = time.time()
    print(et - st)
    return resultD()


def start():
    content = open("./Original.txt", "r")
    content.seek(0)
    first_char = content.read(1)
    if not first_char:
        return render_template("EmptyD.html")
    else:
        return render_template("OptionD.html")


@app.route("/indexD")
def indexD():
    # Check if the user is logged in, and display index.html if logged in
    if "user_id" in session:
        return render_template("indexD.html")
    # If not logged in, you can redirect to a login page or display a message
    else:
        return redirect(url_for("main1"))  # Redirect to main() if not logged in


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/return-files-data/")
def return_files_data():
    try:
        return send_file("./Output.txt", as_attachment=True, download_name="Output.txt")
    except Exception as e:
        return str(e)


@app.route("/data2/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("NofileD.html")
        file = request.files["file"]
        if file.filename == "":
            return render_template("NofileD.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], "Original.txt"))
            return start()

        return render_template("InvalidD.html")


@app.route("/")
def main1():
    return render_template("main1.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
