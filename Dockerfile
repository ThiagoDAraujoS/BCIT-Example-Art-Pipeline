FROM python:3.10
RUN mkdir /pipeline/
WORKDIR /pipeline/
COPY requirements.txt /pipeline/requirements.txt
RUN pip install -r requirements.txt
COPY . /pipeline/
EXPOSE 5000
CMD ["python", "main.py"]
