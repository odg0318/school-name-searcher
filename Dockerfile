FROM python:2

RUN apt-get update && apt-get install -y --no-install-recommends \
            g++ \
            openjdk-7-jdk \
            python-dev

WORKDIR /application

ADD school/ school/ 
ADD main.py requirements.txt /application/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
