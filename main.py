from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
import json

app = Flask(__name__)

API_KEY = "TopSecretAPIKey"


# CREATE DB
class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def convert_instance_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "map_url": self.map_url,
            "img_url": self.img_url,
            "location": self.location,
            "amenities": {
                "seats": self.seats,
                "has_toilet": self.has_toilet,
                "has_wifi": self.has_wifi,
                "has_sockets": self.has_sockets,
                "can_take_calls": self.can_take_calls,
                "coffee_price": self.coffee_price,
            }
        }


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Search Cafe by Location and Amenities:
@app.route("/search", methods=["GET"])
def search():
    location_query = request.args.get('location')
    has_wifi = request.args.get('has_wifi')
    has_sockets = request.args.get('has_sockets')
    can_take_calls = request.args.get('can_take_calls')

    # Start the query with all cafes
    query = Cafe.query

    # Apply filters only if they are checked (true)
    if location_query:
        query = query.filter(Cafe.location.ilike(f"%{location_query}%"))

    if has_wifi == 'true':
        query = query.filter(Cafe.has_wifi == True)

    if has_sockets == 'true':
        query = query.filter(Cafe.has_sockets == True)

    if can_take_calls == 'true':
        query = query.filter(Cafe.can_take_calls == True)

    # Get all cafes if no filters applied (no filter variables passed)
    cafes = query.all()

    if cafes:
        cafes_list = [cafe.convert_instance_to_dict() for cafe in cafes]
        return jsonify(cafes=cafes_list)
    else:
        return jsonify({"error": "No cafes found"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
