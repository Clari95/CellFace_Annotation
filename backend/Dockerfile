FROM python:3.7-buster
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt .
COPY start_server.sh .
RUN apt-get update && \
  LC_ALL=C DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    ldap-utils \
    libldap2-dev \
    libsasl2-dev \
    slapd
RUN pip install -r requirements.txt
CMD ["sh", "./start_server.sh"]
