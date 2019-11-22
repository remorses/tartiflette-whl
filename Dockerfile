FROM python:3.7.4-alpine

RUN apk add --no-cache build-base libffi-dev openssl-dev

RUN pip install --index-url  https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple tartiflette-test-with-wheels

COPY roba/tt_test.py /tt_test.py

RUN python /tt_test.py

