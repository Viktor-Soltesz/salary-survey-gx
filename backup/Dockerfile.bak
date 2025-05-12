FROM python:3.8.5

# install system packages
RUN apt-get update && apt-get install --no-install-recommends -y \
        git \ 
        libpq-dev \
        python3-dev \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir great_expectations \
    && pip install --no-cache-dir sqlalchemy==1.4.25 \
    && pip install --no-cache-dir pybigquery \
    && pip install --no-cache-dir sqlalchemy_bigquery \
    && pip install --no-cache-dir black
ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8

# Install gcloud
# TODO: test if gcloud is required
RUN mkdir -p /usr/local/gcloud \
    && curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-392.0.0-linux-x86_64.tar.gz \
    && tar -C /usr/local/gcloud -xf google-cloud-cli-392.0.0-linux-x86_64.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh --quiet \
    && rm google-cloud-cli-392.0.0-linux-x86_64.tar.gz
ENV PATH=$PATH:/usr/local/gcloud/google-cloud-sdk/bin/

ENTRYPOINT ["/usr/local/bin/great_expectations"]
CMD ["--help"]