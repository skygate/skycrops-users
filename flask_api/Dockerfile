FROM python:3.7
RUN apt update -y
RUN apt install -y libpython3.7-dev cmake

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run_flask"]
