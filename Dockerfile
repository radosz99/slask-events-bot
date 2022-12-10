FROM python:3.8

RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN  apt-get update
RUN  apt-get install -y --no-install-recommends firefox

WORKDIR /usr/app/src
COPY . ./
RUN pip install -r requirements.txt

ENV PATH="${PATH}:/usr/app/src"
COPY constants.py ./
CMD ["python", "./main.py"]
