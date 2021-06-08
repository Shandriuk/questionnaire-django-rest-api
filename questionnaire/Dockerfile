FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir -p questionnare

WORKDIR questionnare
COPY requirements.txt /questionnare/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . questionnare/ 
