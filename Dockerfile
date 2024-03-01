# Use an official Python runtime as a parent image
FROM ubuntu:latest

LABEL authors='Tridib Basumatary'

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN  apt-get update &&  apt-get install -y python3-pip
# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Use Gunicorn to serve the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_blog1.wsgi:application"]
