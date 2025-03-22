from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app = Flask(__name__)
app.secret_key = "1234"  # Change this!

# Store hashed password
PASSWORD_HASH = hashlib.sha256("1234".encode()).hexdigest()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        entered_password = request.form["password"]
        if hashlib.sha256(entered_password.encode()).hexdigest() == PASSWORD_HASH:
            session["authenticated"] = True
            return redirect(url_for("protected"))
        else:
            return "❌ Incorrect password! Try again."

    return render_template("login.html")

@app.route("/protected")
def protected():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return "<h1>🔒 Welcome to the protected page!</h1> <a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
