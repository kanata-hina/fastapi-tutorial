FROM python:3.9

RUN pip install fastapi uvicorn

EXPOSE 8080

COPY ./api /api

CMD ["uvicorn", "api.main:api", "--reload", "--host", "0.0.0.0", "--port", "8080"]