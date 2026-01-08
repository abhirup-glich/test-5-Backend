FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5001

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5001"]
