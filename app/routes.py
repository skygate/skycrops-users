import io

from flask import request, jsonify, Blueprint

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
from .models import User

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

    user = User(username=name, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"status": f"{name} saved to the database."})


@api.route("/users/database", methods=["POST"])
def show_database():
    users = User.query.all()
    return jsonify({"users": users})


@api.route("/users/database/clear", methods=["POST"])
def clear_database():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return jsonify({"status": "Database clear!"})


@api.route("/generate_mapping", methods=["POST"])
def generate_mapping():
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

    trees_generator.plot_coordinates()

    return jsonify({"status": "Map generated successfully!"})
