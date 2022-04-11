# This is docker file
FROM python:3.10
WORKDIR /multiprojs
RUN conda create --name web --file requirements.txt
RUN conda activate web
COPY requirements.txt requirements.txt
RUN echo "installing dependencies"
RUN !pwd
