ARG IMAGE_VERSION=3.11.0a1-alpine
FROM python:${IMAGE_VERSION}

LABEL image.os="alpine"
LABEL image.name="py3-selenium"
LABEL owner="Chris Herrera"
LABEL maintainer="christian@christian-herrera.com"
LABEL license="MIT"

# Headless support using Firefox driver
# ttf-dejavu required for Firefox page rendering
RUN apk upgrade --update-cache --available \
    && apk update \
    && apk add --no-cache xvfb firefox dbus ttf-dejavu ca-certificates

RUN mkdir -p /etc/local.d/
COPY --chown=root:root ./bash/Xvfb.start /etc/local.d/Xvfb.start
RUN chmod 755 /etc/local.d/Xvfb.start

COPY requirements.txt /tmp/
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r /tmp/requirements.txt

RUN find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip

ENV PYTHONUNBUFFERED 1

CMD ['python', '-h']