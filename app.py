from asyncio import all_tasks
from flask import Flask,render_template,url_for,redirect,session,request
from flask_pymongo import PyMongo
import bcrypt
# ObjectId function is used to convert the id string to an objectid that MongoDB can understand
from bson.objectid import ObjectId
from pymongo import MongoClient



app =Flask(__name__)
app.secret_key='testing'
client = MongoClient("mongodb+srv://aniketsrivastava57:Samsung@cluster0.qzmq4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database('total_records')
records = db.register


#assign URLs to have a particular route 
@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    #if method post in index
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            records.insert_one(user_input)
            
            #find the new created account and its email
            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            #if registered redirect to logged in as the registered user
            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
  if request.method == "POST":   # if the request method is post, then insert the todo document in todos collection
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('logged_in')) # redirect the user to home page
        all_todos = todos.find()    # display all todo documents
  return render_template('logged_in.html', todos = all_tasks) 
        
@app.post("/<id>/delete/")
def delete(id): #delete function by targeting a todo document by its own id
    todos.delete_one({"_id":ObjectId(id)}) #deleting the selected todo document by its converted id
    return redirect(url_for('logged_in')) # again, redirecting you to the home page
db = client.flask_database # creating your flask database using your mongo client 
todos = db.todos # creating a collection called "todos"
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')




if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)
