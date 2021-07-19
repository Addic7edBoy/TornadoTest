FROM python:3.6

WORKDIR /basic

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y netcat

COPY alembic alembic
COPY alembic.ini basic.py ./

EXPOSE 8888

# CMD ["python3", "./basic.py"]
ENTRYPOINT [ "/bin/bash", "./boot.sh" ]
