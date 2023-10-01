from routes import routes_bp
from backend.usersHandler import users_bp

from flask import Flask


app = Flask(__name__)

app.register_blueprint(routes_bp, url_prefix='/')
app.register_blueprint(users_bp, url_prefix='/users')


# 
# Section: RUN
# 

def run():
    app.run(host='localhost', port=8000)