FROM python:3.6.6-alpine3.8

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY helm.py /bin/
COPY template_config /root/.kube/template_config

ENTRYPOINT ["/bin/sh"]
