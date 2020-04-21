from app import application

from config import HOST


@application.shell_context_processor
def make_shell_context():
    pass


if __name__ == "__main__":
    application.run(debug=True, host=HOST)
