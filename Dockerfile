FROM tiangolo/uvicorn-gunicorn:python3.8-slim 

#change wordir for the production file to /app
WORKDIR ./
# ENV DEBIAN_FRONTEND=noninteractive
ENV MODULE_NAME=app 
CMD ["echo", "Hello world"]

# RUN apt-get update \        
#      apt-get install -y git

# ADD requirements.txt . 
# RUN pip install -r requirements.txt \    
#     && rm -rf /root/.cache 
