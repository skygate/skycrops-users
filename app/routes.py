import io

from flask import request, jsonify, Blueprint

from config import COORDS_KEY
from .helpers import utils

api = Blueprint("api", __name__)


@api.route("/healthchecker", methods=["GET"])
def healthchecker():
    return jsonify({"status": "I am alive!"}), 200


@api.route("/generate_mapping", methods=["POST"])
def generate_mapping():
    coords = request.files.get(COORDS_KEY)

    if not coords:
        return jsonify({"status": "Failed! Coordinates can't be empty!"}), 400

    if not coords.filename.endswith(".csv"):
        return jsonify({"status": "Failed! Coordinates file must have a .csv extension!"}), 400

    decoded_coords = io.StringIO(coords.stream.read().decode("UTF8"), newline=None)
    listed_coords = utils.read_coordinates(decoded_coords)
    print(listed_coords)

    return jsonify({"status": "Map generated successfully!"})
