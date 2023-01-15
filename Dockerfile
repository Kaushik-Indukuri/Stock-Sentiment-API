FROM python:3.9
ARG PORT=80
ENV PORT=$PORT

RUN echo "Port is $PORT"

WORKDIR /app

ENV PORT

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=$PORT"]