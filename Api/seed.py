from faker import Faker
from app import app, db
from models import User, Location, Weather
from werkzeug.security import generate_password_hash

fake = Faker()

def clear_db():
    db.drop_all()
    db.create_all()

def seed_users(n):
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
        )
        user.set_password("password")  # Set a default password for all users
        db.session.add(user)
    db.session.commit()

def seed_locations(n):
    users = User.query.all()
    location_names = [
        "Nairobi", "Kakamega", "Elementaita", "Voi",
        "Machakos", "Mombasa", "Limuru", "Nakuru", "Eldoret", "Kisumu"
    ]
    used_locations = set()

    for _ in range(n):
        while True:
            location_name = fake.random_element(location_names)
            if location_name not in used_locations:
                used_locations.add(location_name)
                break

        location = Location(
            name=location_name,
            latitude=fake.latitude(),
            longitude=fake.longitude(),
            user_id=fake.random_element(users).id
        )
        db.session.add(location)
    db.session.commit()

def seed_weathers(n):
    locations = Location.query.all()
    for _ in range(n):
        weather = Weather(
            temperature=fake.random_number(digits=2),
            description=fake.word(ext_word_list=[
                "clear sky", "few clouds", "scattered clouds", "broken clouds",
                "shower rain", "rain", "thunderstorm", "snow", "mist"
            ]),
            location_id=fake.random_element(locations).id
        )
        db.session.add(weather)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        clear_db()
        seed_users(10)
        seed_locations(10)  
        seed_weathers(50)
        print("Database seeded!")
