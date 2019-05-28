FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP app
ENV FLASK_ENV development
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]