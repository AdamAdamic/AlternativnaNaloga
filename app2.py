import os
import time
from flask import Flask, render_template, request, redirect, session, jsonify
from tinydb import TinyDB, Query
from werkzeug.utils import secure_filename


app = Flask(name, template_folder="templates2")
app.secret_key = "Leave_no_one_alive"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

BAZE
db = TinyDB("db2.json")
users = db.table("users")
posts = db.table("posts")
Uporabnik = Query()
Objava = Query()
likes_db = db.table("likes")
Like = Query()

@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    vse_objave = posts.all()
    return render_template("index2.html", objave=reversed(vse_objave), uporabnik=session["user"])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.search(Uporabnik.username == username):
            return "Uporabnik obstaja"
        users.insert({"username": username, "password": password})
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(Uporabnik.username == username)
        if user and user["password"] == password:
            session["user"] = username
            return redirect("/")
    return render_template("login.html")
@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session: 
        return redirect("/login")

    file = request.files.get('slika')
    desc = request.form.get('opis', '')

    if file and file.filename != '':
        # Ustvarimo unikaten ID za objavo, da bo LIKE deloval!
        post_id = str(int(time.time() * 1000)) 
        fname = secure_filename(file.filename)
        unique_name = f"{postid}{fname}"

Prepričaj se, da mapa obstaja
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_name))

        post_id = str(int(time.time() * 1000)) # Ustvarimo unikaten ID

        posts.insert({
        "id": post_id, # potreben je ID
        "avtor": session["user"],
        "slika_url": unique_name,
        "opis": desc,
        "likes": 0
        })
        return redirect("/dashboard")
@app.route("/like", methods=["POST"])
def like_post():
    if "user" not in session:
        return jsonify({"error": "Ni prijave"}), 401

    postid = request.form.get("id")
    uporabnik = session["user"]

preveri, če je ta uporabnik to objavo že všečkal
    ze_vseckal = likes_db.search((Like.post_id == postid) & (Like.user == uporabnik))


    #dobimo podatke 
    post = posts.get(Objava.id == postid)
    if not post:
        return jsonify({"error": "Ni objave"}), 404

    if not ze_vseckal:
        # UPORABNIK ŠE NI VŠEČKAL -> Dodaj všeček
        novi_likes = post.get("likes", 0) + 1
        posts.update({"likes": novi_likes}, Objava.id == postid)
        # Zabeleži v bazo likes, da ne more ponoviti
        likes_db.insert({"post_id": postid, "user": uporabnik})
        status = "vseckano"
    else:
        # UPORABNIK JE ŽE VŠEČKAL -> Odstrani všeček (Unlike)
        novi_likes = max(0, post.get("likes", 0) - 1)
        posts.update({"likes": novi_likes}, Objava.id == postid)
        # Izbriši zapis iz tabele likes
        likes_db.remove((Like.post_id == postid) & (Like.user == uporabnik))
        status = "odvseckano"

    return jsonify({"new_likes": novi_likes, "id": postid, "status": status})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if name == "main":
    app.run(debug=True)