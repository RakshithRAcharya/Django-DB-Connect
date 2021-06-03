FROM ubuntu:18.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update
RUN apt-get install -y python3.8
RUN apt install -y python3-pip

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip3 install --upgrade pip 
COPY ./requirements.txt /usr/src/app
RUN pip3 install virtualenv
RUN apt-get install -y python3-venv
RUN python3 -m venv sample
RUN source sample/bin/activate
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt --no-cache-dir

# copy project
COPY . /usr/src/app

EXPOSE 8000

ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
