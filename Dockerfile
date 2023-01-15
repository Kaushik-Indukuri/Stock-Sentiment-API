ARG port_var=80
FROM python:3.9

RUN echo "Port is $port_var"
RUN echo "$PORT"

WORKDIR /app

ENV PORT

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=$port_var"]