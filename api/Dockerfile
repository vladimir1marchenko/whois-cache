FROM python:3.12-alpine3.19
RUN apk add --no-cache bash curl

COPY ./ /opt/api/
WORKDIR /opt/api

RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
