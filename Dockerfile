FROM public.ecr.aws/lambda/python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["src/main.handler"]
CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--reload"]