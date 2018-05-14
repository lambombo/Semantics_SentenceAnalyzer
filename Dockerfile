FROM python:3.6-alpine

COPY app app
COPY flask_manage.py config.py boot.sh requirements.txt ./

RUN pip install -r ./requirements.txt

EXPOSE 5000
RUN chmod +x ./boot.sh
CMD sh ./boot.sh
