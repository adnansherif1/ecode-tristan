# FROM tiangolo/uvicorn-gunicorn:python3.8-slim 
FROM python:3.8

#change wordir for the production file to /app
WORKDIR /app
# WORKDIR /app
# ENV DEBIAN_FRONTEND=noninteractive
ENV MODULE_NAME=app 

RUN apt update
RUN apt-get install -y git        

CMD git clone $repo /app && pip install -r requirements.txt \    
    && rm -rf /root/.cache && uvicorn app.main:app --host 0.0.0.0 --port 80

#https://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@github.com/adnansherif1/ecode-tristan.git

# ADD requirements.txt . 
# RUN pip install -r requirements.txt \    
#     && rm -rf /root/.cache 
