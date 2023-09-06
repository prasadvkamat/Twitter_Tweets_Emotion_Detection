
from flask import Flask, request, render_template,redirect,session, url_for
import pandas as pd
import sqlite3 as sql
import pandas

import os;
os.environ['KERAS_BACKEND'] = 'theano'
import pandas as pd
from emotion_predictor import EmotionPredictor


app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret key'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods = ["GET","POST"])
def signup():
    msg=None
    if(request.method=="POST"):
        if (request.form["uname"]!="" and request.form["uphone"]!="" and request.form["username"]!="" and request.form["upassword"]!=""):
            username=request.form["username"]
            password=request.form["upassword"]
            uname=request.form["uname"]
            uphone=request.form["uphone"]


            with sql.connect("tweets.db") as con:
                c=con.cursor()
                c.execute("INSERT INTO  signup VALUES('"+uname+"','"+uphone+"','"+username+"','"+password+"')")
                msg = "Your account is created"

                con.commit()
        else:
            msg="Something went wrong"


    return render_template("signup.html", msg=msg)

@app.route("/contactus", methods = ["GET","POST"])
def contactus():
    msg=None
    if(request.method=="POST"):
        if (request.form["name"]!="" and request.form["email"]!="" and request.form["phone"]!="" and request.form["message"]!=""):
            name1=request.form["name"]
            email1=request.form["email"]
            phone1=request.form["phone"]
            message1=request.form["message"]


            with sql.connect("flight.db") as con:
                c=con.cursor()
                c.execute("INSERT INTO  contact VALUES('"+name1+"','"+email1+"','"+phone1+"','"+message1+"')")
                msg = "your contact details has sent"

                con.commit()
        else:
            msg="Something went wrong"


    return render_template("contact.html", msg=msg)

@app.route('/userlogin')
def userlogin():
    return render_template("userlogin.html")

@app.route('/userlogout')
def userlogout():
	# Remove the session variable if present
	session.clear()
	return redirect(url_for('home'))

@app.route('/userloginNext',methods=['GET','POST'])
def userloginNext():
    msg=None
    if (request.method == "POST"):
        username = request.form['username']
      
        upassword = request.form['upassword']
        
        with sql.connect("tweets.db") as con:
            c=con.cursor()
            c.execute("SELECT username,upassword  FROM signup WHERE username = '"+username+"' and upassword ='"+upassword+"'")
            r=c.fetchall()
            for i in r:
                if(username==i[0] and upassword==i[1]):
                    session["logedin"]=True
                    session["username"]=username
                    return redirect(url_for("userhome"))
                else:
                    msg= "please enter valid username and password"
    
    return render_template("userlogin.html",msg=msg)

@app.route('/userhome')
def userhome():
    return render_template("userhome.html")


@app.route('/userpredict')
def userpredict():
    return render_template("tweetprediction.html")

@app.route('/usergallery')
def usergallery():
    return render_template("usergallery.html")

@app.route("/predict", methods = ["GET", "POST"])

def predict():
# Pandas presentation options
   
    if request.method == "POST":

        tweets=[]
        tweet1=request.form["tweets"]
        tweets += [tweet1]
    
        
     
        model = EmotionPredictor(classification='ekman', setting='mc', use_unison_model=True)
        
         
        print(tweets)
        predictions = model.predict_classes(tweets)
        print(predictions, '\n')

        
        probabilities = model.predict_probabilities(tweets)
        print(probabilities, '\n')

        embeddings = model.embed(tweets)



        df = pd.DataFrame(predictions, columns= ['Tweet', 'Emotion'])

        df.to_csv (r'C:\project\Tweets_Detection\Tweets_Detection\predictonresult.csv', index = False, header=True)

        df1 = pd.DataFrame(probabilities, columns= ['Tweet','Tweet','Anger','Disgust','Fear','Joy','Sadness','Surprise'])

        df1.to_csv (r'C:\project\Tweets_Detection\Tweets_Detection\probabilities.csv', index = False, header=True)
        output= "Data inserted successfully"
        return render_template('tweetprediction.html',prediction_text=" {}".format(output))   
    return render_template("tweetprediction.html")

if __name__ == "__main__":
    app.run(debug=True)
