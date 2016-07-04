FROM python:2.7-alpine

MAINTAINER jace@xuh.me

ADD . /jetkeys
WORKDIR /jetkeys

RUN pip install --no-cache -U pip \
    && pip install --no-cache -r requirements.txt

ENTRYPOINT ["/jetkeys/entrypoint.sh"]
CMD ["python", "main.py"]