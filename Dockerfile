FROM python:3.9

WORKDIR /server

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY requirements.txt requirements.txt
RUN pip install --default-timeout=1000 -r requirements.txt

COPY . .
RUN mkdir -p videos_storage
RUN mkdir -p images_storage

CMD [ "python", "./server.py"]