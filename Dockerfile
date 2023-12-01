FROM python:2
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN ./setup.py install
VOLUME /code/storage/
CMD ["./docker-entry.sh"]
