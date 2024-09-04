FROM python:3.11 

WORKDIR /

COPY . /

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
