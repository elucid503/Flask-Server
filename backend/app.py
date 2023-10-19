from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Check if DB directory exists 




@app.route('/CreateAccount', methods=['POST'])
def Login():
    # Get the username and password from the request body
    UserName = request.form.get('username')
    Password = request.form.get('password')

    if not UserName or not Password:
        return make_response(LoginElement("Missing username or password", False).ToHTML())

    # Check if the db directory 

    # Create a new user from the username and password
    CreatedUser = User(UserName, Password)
    User.Save()

    # Set cookie to the username
    Response = make_response(LoggedInElement("Logged in successfully", True, CreatedUser).ToHTML())
    Response.set_cookie('username', UserName)

    return Response

class User:
    def __init__(self, UserName, Password):
        self.UserName = UserName
        self.Password = Password
        self.Data = {}

    def AddData(self, Key, Value):
        self.Data[Key] = Value
    
    def Save(self):
        # Save the user to the database
        path = f"./store/users/{self.UserName}.json"
        with open(path, 'w') as f:
            f.write(json.dumps(self.Data))
            f.close()
        return True

class LoginElement:
    def __init__(self, Message, Success):
        self.Message = Message
        self.Success = Success

    def ToHTML(self):
        return f"""
        <div class='form-group'>
            <label for='username'>Username</label>
            <input type='text' name='username' id='username' class='form-control'/>
        </div>
        <div class='form-group'>
            <label for='password'>Password</label>
            <input type='password' name='password' id='password' class='form-control'/>
        </div>
        <div class='form-group'>
            {self.Success and f'<p>{self.Message}</p>' or f"<p style='color: red;'>{self.Message}</p>"}
            <input type='submit' name='submit' id='submit' value='Login' class='btn btn-primary'/>
        </div>"""

class LoggedInElement:
    def __init__(self, Message, Success, User):
        self.Message = Message
        self.Success = Success
        self.User = User

    def ToHTML(self):
        return f"""<div class='LoggedInElement'>
            <p>Logged in successfully</p>
            <p>Username: {self.User.UserName}</p>
            <p>Password: {self.User.Password}</p>
        </div>"""

if __name__ == '__main__':
    app.run(debug=False)
