FROM chrisherrera/py3-selenium

LABEL image.os="alpine"
LABEL image.name="py3-selenium"
LABEL owner="Chris Herrera"
LABEL maintainer="christian@christian-herrera.com"
LABEL license="MIT"

RUN mkdir /app

COPY ./python/*.py /app/

CMD ['python', '-h']