from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template('signup.html', title="Signup!")


@app.route("/", methods=['POST'])
def validate_form():
    username = request.form["username"]
    password = request.form["password"]
    verifypass = request.form["verifypass"]
    email = request.form["email"]
    username_error = ""
    password_error = ""
    veripass_error = ""
    email_error = ""

    #validate username
    if username == "":
        username_error = "Please enter a Username"
    else:
        special = " !@#$%^&*(){}[]~`';:><,.?" + '"'
        for char in username:
            if char in special:
                username_error = "Usernames cannot contain spaces or special characters"
                break
        if len(username) < 3 or len(username) > 20:
            username_error = "Usernames must be 3-20 characters"
    
    #validate password
    if password == "": 
        password_error = "Please enter a password"
    else:
        if " " in password:
            password_error = "Passwords cannot contain spaces"
        if len(password) < 3 or len(password) > 20:
            password_error = "Passwords must be 3-20 characters"
    
    #validate password confirmation
    if verifypass == "":
        veripass_error = "Please verify your password"
    if password != verifypass:
        veripass_error = "This must match your password"
    
    #validate email
    if email != "":
        if email.count("@", 1, -4) != 1 or email.count(".", -4, -2) != 1 or " " in email:
            email_error = "Please enter a valid email address"

    if username_error == "" and password_error == "" and veripass_error == "" and email_error == "":
        return redirect("/success?username?email", code=307)
    
    return render_template('signup.html', title="Signup!", 
        username=username, password=password, 
        verifypass=verifypass, email=email, 
        username_error=username_error, password_error=password_error, 
        veripass_error=veripass_error, email_error=email_error)


@app.route("/success", methods=['POST'])
def successful():
    username = request.form["username"]
    email = request.form["email"]

    return render_template('success.html', 
        title="Registration Successful!", 
        username=username, email=email)

app.run()