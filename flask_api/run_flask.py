from app import application, db
from app.models import User, Orchard
from config import HOST


@application.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Orchard": Orchard}


if __name__ == "__main__":
    application.run(debug=True, host=HOST, ssl_context=('cert.pem', 'key.pem'))
