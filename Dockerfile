FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Install Gunicorn
RUN pip install gunicorn

# Run Gunicorn with infinite timeout
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "0", "app:app"]
