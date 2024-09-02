# Use an official Python runtime as a parent image
FROM python:3.8

# Install git, ffmpeg, and other necessary dependencies
RUN apt-get update && apt-get install -y git ffmpeg && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir git+https://github.com/openai/whisper.git flask torch ffmpeg-python

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Run app.py when the container launches
CMD ["python", "app.py"]