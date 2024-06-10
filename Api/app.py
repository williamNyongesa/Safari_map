from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, User, Location, Weather
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Index(Resource):
    def get(self):
        return {"message": "Welcome to My Safari Map!"}

class UserResource(Resource):
    @login_required
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {"username": user.username, "email": user.email}

class LocationResource(Resource):
    @login_required
    def get(self, location_id):
        location = Location.query.get_or_404(location_id)
        return {
            "name": location.name,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "user_id": location.user_id
        }

class WeatherResource(Resource):
    @login_required
    def get(self, location_id):
        weather = Weather.query.filter_by(location_id=location_id).first_or_404()
        return {
            "temperature": weather.temperature,
            "description": weather.description,
            "timestamp": weather.timestamp.isoformat()
        }

class Register(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {"message": "User already exists"}, 400
        
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            login_user(user)
            return {"message": "Logged in successfully"}, 200
        else:
            return {"message": "Invalid username or password"}, 400

class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {"message": "Logged out successfully"}, 200

api.add_resource(Index, '/')
api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(LocationResource, '/location/<int:location_id>')
api.add_resource(WeatherResource, '/location/<int:location_id>/weather')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == "__main__":
    app.run(debug=True)
