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
            return redirect(url_for("index"))  # Redirect to index() after successful login
        else:
            flash("Login failed. Please check your credentials.", "error")

        connection.close()

    return render_template("login.html")

# Logout route
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main"))  # Redirect to main() after logout

def resultE():
    path = "./Segments"
    dir_list = os.listdir(path)
    print(dir_list)
    return render_template("Result.html", dir_list=dir_list)

@app.route("/encrypt/")
def EncryptInput():
    Segment()
    gatherInfo()
    HybridCrypt()
    return resultE()

def start():
    content = open("./Original.txt", "r")
    content.seek(0)
    first_char = content.read(1)
    if not first_char:
        return render_template("Empty.html")
    else:
        return render_template("Option.html")

# Updated index route to display index.html
@app.route("/index")
def index():
    # Check if the user is logged in, and display index.html if logged in
    if "user_id" in session:
        return render_template("index.html")
    # If not logged in, you can redirect to a login page or display a message
    else:
        return redirect(url_for("main"))  # Redirect to main() if not logged in

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/return-files-key/")
def return_files_key():
    try:
        return send_file(
            "./Original.txt", as_attachment=True, download_name="Original.txt"
        )
    except Exception as e:
        return str(e)

@app.route("/data/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("Nofile.html")
        file = request.files["file"]
        if file.filename == "":
            return render_template("Nofile.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], "Original.txt"))
            return start()

        return render_template("Invalid.html")

# Main route to display the main.html page
@app.route("/")
def main():
    return render_template("main.html")

if __name__ == "__main__":
    create_users_table()  # Initialize the database
    app.run(debug=True)
