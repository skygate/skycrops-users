import io

from flask import request, jsonify, Blueprint
from flask_login import current_user, login_user, logout_user

from config import (
    USERNAME_KEY,
    PASSWORD_KEY,
    COORDS_KEY,
    ROWS_KEY,
    TREES_KEY,
    DEFAULT_ROWS_DISTANCE,
    DEFAULT_TREES_DISTANCE,
)
from . import db
from .helpers import utils
from .helpers.generate_trees import TreesGenerator
from .models import User, Orchard

api = Blueprint("api", __name__)


@api.route("/healthchecker", methods=["GET"])
def healthchecker():
    return jsonify({"status": "I am alive!"}), 200


@api.route("/users", methods=["POST"])
def create_user():
    name = request.form.get(USERNAME_KEY)
    if not name:
        return jsonify({"status": "Name can't be empty."}), 400

    password = request.form.get(PASSWORD_KEY)
    if not password:
        return jsonify({"status": "Password can't be empty."}), 400

    is_name_duplicated = User.query.filter_by(username=name).first()
    if is_name_duplicated:
        return (
            jsonify(
                {"status": "This name is already used, please use a different one."}
            ),
            400,
        )

    user = User(username=name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"status": f"{name} saved to the database."})


@api.route("/users/database", methods=["POST"])
def show_database():
    users = User.query.all()
    orchards = Orchard.query.all()
    return jsonify({"status": [{"users": f"{users}"}, {"orchards": f"{orchards}"}]})


@api.route("/users/database/clear", methods=["POST"])
def clear_database():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return jsonify({"status": "Database clear!"})


@api.route("/users/orchards", methods=["POST"])
def create_orchard():
    if not current_user.is_authenticated:
        return jsonify({"status": "You have to login first!"}), 400

    coords = request.files.get(COORDS_KEY)
    distance_between_rows = request.form.get(ROWS_KEY)
    distance_between_trees = request.form.get(TREES_KEY)

    if not coords:
        return jsonify({"status": "Failed! Coordinates can't be empty!"}), 400

    if not coords.filename.endswith(".csv"):
        return (
            jsonify({"status": "Failed! Coordinates file must have a .csv extension!"}),
            400,
        )

    if not distance_between_rows:
        distance_between_rows = DEFAULT_ROWS_DISTANCE
    else:
        try:
            distance_between_rows = float(distance_between_rows)
        except ValueError:
            return (
                jsonify(
                    {"status": "Failed! Distance between rows must be a float number!"}
                ),
                400,
            )

    if not distance_between_trees:
        distance_between_trees = DEFAULT_TREES_DISTANCE
    else:
        try:
            distance_between_trees = float(distance_between_trees)
        except ValueError:
            return (
                jsonify(
                    {"status": "Failed! Distance between trees must be a float number!"}
                ),
                400,
            )

    decoded_coords = io.StringIO(coords.stream.read().decode("UTF8"), newline=None)
    listed_coords = utils.read_coordinates(decoded_coords)

    trees_generator = TreesGenerator(
        listed_coords, distance_between_rows, distance_between_trees
    )
    trees_coordinates = trees_generator.get_trees_coords()
    rows = trees_generator.number_of_rows
    trees = trees_generator.number_of_trees_in_each_row

    orchard = Orchard(rows=rows, trees=trees, author=current_user)
    db.session.add(orchard)
    db.session.commit()

    return jsonify({"status": f"{coords.filename} saved to the database."})


@api.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return jsonify({"status": "Failed! Someone is already logged in!"}), 400

    name = request.form.get(USERNAME_KEY)
    if not name:
        return jsonify({"status": "Name can't be empty."}), 400

    password = request.form.get(PASSWORD_KEY)
    if not password:
        return jsonify({"status": "Password can't be empty."}), 400

    user = User.query.filter_by(username=name).first()
    if not user or not user.check_password(password):
        return jsonify({"status": "Invalid username or password"}), 400

    login_user(user)
    return jsonify({"status": f"{name} logged in successfully!"})


@api.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"status": "Successfully logged out!"})


@api.route("/orchards", methods=["POST"])
def get_orchards_data():
    if not current_user.is_authenticated:
        return jsonify({"status": "You have to login first!"}), 400
    orchards = current_user.orchards.all()
    orchards_json = [
        [
            {"id": orchard.id},
            {"rows": orchard.rows},
            {"trees in each row": orchard.trees},
        ]
        for orchard in orchards
    ]
    return jsonify({"orchards": f"{orchards_json}"})


@api.route("/is_logged", methods=["POST"])
def is_logged():
    return jsonify({"status": current_user.is_authenticated})
