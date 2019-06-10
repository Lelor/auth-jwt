FROM python:latest
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m unittest
ENV FLASK_APP api
ENV FLASK_ENV development
EXPOSE 8000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]