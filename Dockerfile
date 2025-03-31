FROM python:3.9

RUN mkdir /fastapi_url_shortener

WORKDIR /fastapi_url_shortener

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/app.sh

#WORKDIR app

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]