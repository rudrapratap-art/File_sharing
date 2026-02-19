import os
from flask import Flask, render_template, request, redirect, session
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# ---------------- LOAD ENV ----------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_123")


# ---------------- DATABASE ----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------- ADMIN ----------------
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")


# ---------------- USER MODEL ----------------
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)


# Create DB
with app.app_context():
    db.create_all()


# ---------------- STORAGE METER ----------------
def get_storage_usage():

    try:
        usage = cloudinary.api.usage()

        storage = usage.get("storage")

        if storage and storage.get("limit_bytes"):

            used_bytes = storage["used_bytes"]
            limit_bytes = storage["limit_bytes"]

        else:
            raise Exception("Usage API not available")

    except Exception as e:

        print("Using manual storage calculation...", e)

        resources = cloudinary.api.resources(
            type="upload",
            max_results=500
        )

        files = resources.get("resources", [])

        used_bytes = sum(f.get("bytes", 0) for f in files)

        # Free plan approx limit (25GB)
        limit_bytes = 25 * 1024 * 1024 * 1024


    used_mb = round(used_bytes / (1024 * 1024), 2)
    limit_mb = round(limit_bytes / (1024 * 1024), 2)

    percent = round((used_bytes / limit_bytes) * 100, 2)

    return used_mb, limit_mb, percent


# =================================================
# HOME (PUBLIC VIEW + LOGIN REQUIRED UPLOAD)
# =================================================
@app.route("/", methods=["GET", "POST"])
def home():

    message = ""
    file_url = ""

    # Upload
    if request.method == "POST":

        # Login required
        if not session.get("user"):
            return redirect("/login_user")

        file = request.files.get("file")

        if file:
            try:
                # AUTO = image / video / pdf / docx
                result = cloudinary.uploader.upload(
                    file,
                    resource_type="auto"
                )

                file_url = result["secure_url"]
                message = "Upload Successful ✅"

            except Exception as e:
                message = f"Upload Error: {str(e)}"


    # Get files
    data = cloudinary.api.resources(
        type="upload",
        max_results=100,
        resource_type="auto"
    )

    files = data.get("resources", [])


    # Storage
    used_mb, limit_mb, percent = get_storage_usage()


    return render_template(
        "index.html",

        message=message,
        file_url=file_url,
        files=files,

        used_mb=used_mb,
        limit_mb=limit_mb,
        percent=percent,

        user=session.get("user")
    )


# =================================================
# USER REGISTER
# =================================================
@app.route("/register", methods=["GET", "POST"])
def register():

    msg = ""

    if request.method == "POST":

        user = request.form["username"]
        pwd = request.form["password"]

        if User.query.filter_by(username=user).first():

            msg = "User already exists ❌"

        else:

            hashed = generate_password_hash(pwd)

            new_user = User(username=user, password=hashed)

            db.session.add(new_user)
            db.session.commit()

            return redirect("/login_user")


    return render_template("register.html", msg=msg)


# =================================================
# USER LOGIN
# =================================================
@app.route("/login_user", methods=["GET", "POST"])
def login_user():

    msg = ""

    if request.method == "POST":

        user = request.form["username"]
        pwd = request.form["password"]

        data = User.query.filter_by(username=user).first()

        if data and check_password_hash(data.password, pwd):

            session["user"] = user
            return redirect("/")

        else:
            msg = "Invalid Login ❌"


    return render_template("user_login.html", msg=msg)


# =================================================
# USER LOGOUT
# =================================================
@app.route("/logout_user")
def logout_user():

    session.pop("user", None)
    return redirect("/")


# =================================================
# ADMIN LOGIN
# =================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    msg = ""

    if request.method == "POST":

        user = request.form["username"]
        password = request.form["password"]

        if user == ADMIN_USER and password == ADMIN_PASS:

            session["admin"] = True
            return redirect("/admin")

        else:
            msg = "Invalid Login ❌"


    return render_template("login.html", msg=msg)


# =================================================
# ADMIN PANEL
# =================================================
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")


    data = cloudinary.api.resources(
        type="upload",
        max_results=100,
        resource_type="auto"
    )

    files = data.get("resources", [])


    used_mb, limit_mb, percent = get_storage_usage()


    return render_template(
        "admin.html",

        files=files,

        used_mb=used_mb,
        limit_mb=limit_mb,
        percent=percent
    )


# =================================================
# DELETE (ADMIN ONLY)
# =================================================
@app.route("/delete/<path:public_id>")
def delete_file(public_id):

    if not session.get("admin"):
        return redirect("/login")

    try:
        cloudinary.uploader.destroy(
            public_id,
            resource_type="auto"
        )

    except Exception as e:
        print("Delete Error:", e)


    return redirect("/admin")


# =================================================
# ADMIN LOGOUT
# =================================================
@app.route("/logout")
def logout():

    session.pop("admin", None)
    return redirect("/")


# =================================================
# RUN SERVER (RENDER READY)
# =================================================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
