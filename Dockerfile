# Set base image (host OS)
FROM python:3.12-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
# COPY requirements.txt .
COPY ./requirements.txt /app/requirements.txt

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
# COPY run.py .
# COPY /app/__init__.py .

# # Specify the command to run on container start
# CMD [ "python", "run.py" ]


COPY . /app

ENTRYPOINT ["python"]
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["run.py"]