FROM python:3.6

# copy requirements
COPY requirements.txt requirements.txt
# Install in the default python3 environment
RUN pip install -r requirements.txt --upgrade

RUN mkdir /app

COPY computer.vision.ipynb fashion-mnist_test.csv.gz fashion-mnist_train.csv.gz fashion-mnist-90.h5 LICENSE /app/

WORKDIR /app
