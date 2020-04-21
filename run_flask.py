from app import application


@application.shell_context_processor
def make_shell_context():
    pass


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0")
