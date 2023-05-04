FROM python:3.8-alpine
COPY ./requirements.txt /CLINICA_MEDICA/requirements.txt
WORKDIR /CLINICA_MEDICA
RUN pip install -r requirements.txt
COPY . /CLINICA_MEDICA
ENTRYPOINT [ "python" ]
CMD ["index.py" ]
