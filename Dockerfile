FROM python:3.10

WORKDIR /workspace

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --editable .

CMD [ "api_service", "active" ]