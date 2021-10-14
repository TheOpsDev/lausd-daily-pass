FROM chrisherrera/py3-selenium

LABEL image.os="alpine"
LABEL image.name="py3-selenium"
LABEL owner="Chris Herrera"
LABEL maintainer="christian@christian-herrera.com"
LABEL license="MIT"

# Install pip3 packages
COPY requirements.txt /tmp/
RUN pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r /tmp/requirements.txt

# pip3 cleanup
RUN find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip

RUN mkdir /app
COPY ./python /app/
COPY ./yaml/*.yaml /app/

WORKDIR /app

CMD ['python', 'get_daily_pass.py']