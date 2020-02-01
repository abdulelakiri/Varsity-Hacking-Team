FROM python:3.7.4-slim-buster

ADD . /code
WORKDIR /code

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","-u","app.py"]

