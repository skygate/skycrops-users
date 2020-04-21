from flask import jsonify, Blueprint


api = Blueprint("api", __name__)


@api.route("/healthchecker", methods=["GET"])
def healthchecker():
    return jsonify({"status": "I am alive!"}), 200
