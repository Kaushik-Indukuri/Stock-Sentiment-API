FROM python:3.9
# ARG port_var=80
# ENV PORT=$port_var

# RUN echo "Port is $PORT"

WORKDIR /app

ENV PORT=8000

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

ENTRYPOINT uvicorn src.main:app --host 0.0.0.0 --port $PORT
