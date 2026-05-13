from flask import Flask, render_template, request, redirect, session
from tinydb import TinyDB, Query
import time



app = Flask(
    name,
    template_folder="templates1",
)
app.secret_key = "Stand_ready_for_my_arrival_worm"


db = TinyDB("db1.json")

users = db.table("users")

notes_db = db.table("notes")

User = Query()

Note = Query()



home
@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")


register
@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)

        if users.search(User.username == username):
            return "Uporabnik obstaja"

        users.insert({"username" : username, "password" : password, "note" : ""})
        return redirect("/login")

    return render_template("register.html")
login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        user = users.get(User.username == username)



        if user and user["password"] == password:
            session["user"] = username
            return redirect("/dashboard")
    return render_template("login.html")


dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # Note = Query() mora biti definiran nad funkcijo ali tukaj
    if "user" not in session:
        return redirect("/login")
    #user = users.get(User.username == session["user"])

    vsi_zapiski = notes_db.search(Note.author == session["user"])


    return render_template("index1.html",  zapiski=vsi_zapiski, uporabnik=session["user"])

@app.route("/createNote", methods=["POST"])
def create_note():
    if "user" in session:
        # Ustvari nov prazen zapisek z unikatnim ID
        note_id = str(int(time.time()))
        notes_db.insert({
            "id": note_id, 
            "author": session["user"], 
            "title": "Nov zapisek", 
            "content": ""
        })
        return redirect("/dashboard")
    return "OK"



save_note
@app.route("/saveNote", methods=["POST"])
def saveNote():
    note_id = request.form["id"]
    note = request.form["note"]
    #samo updatamo bazo da se stvari shranijo
    notes_db.update({"note": note}, (Note.id == note_id) & (Note.author == session["user"]))

    return "Saved"
@app.route("/deleteNote", methods=["POST"])
def delete_note():
    if "user" in session:
        note_id = request.form["id"]
        #samo poišče isti note id in istočasno isti author, da ne moreš brisati tujih zapiskov ter izbriše ta zapis iz note
        notes_db.remove((Note.id == note_id) & (Note.author == session["user"]))
        return "Izbrisano"
    return "Unauthorized", 401



logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



app.run(debug = True)
