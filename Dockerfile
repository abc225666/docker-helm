FROM python:3.6.6-alpine3.8

RUN apk add --no-cache curl \
    && curl -o /tmp/helm.tar.gz https://storage.googleapis.com/kubernetes-helm/helm-v2.9.1-linux-amd64.tar.gz \
    && tar xzvf /tmp/helm.tar.gz -C /tmp \
    && mv /tmp/linux-amd64/helm /bin/helm \
    && rm -rf /tmp/*


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY helm.py /bin/
COPY template_config /root/.kube/template_config

ENTRYPOINT ["/bin/helm.py"]
