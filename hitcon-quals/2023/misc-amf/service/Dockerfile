FROM python:slim

RUN pip install Py3AMF

COPY server.py /app/server.py

EXPOSE 5000
CMD ["python", "/app/server.py"]
