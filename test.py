
from flask import Flask,request, render_template,redirect,session, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret key'

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)