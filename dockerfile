FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "application.py"]

RUN pip install newrelic
ENV NEW_RELIC_APP_NAME="devpros-aws-prod"
ENV NEW_RELIC_LOG=stdout
ENV NEW_RELIC_DISTRIBUTED_TRACING_ENABLED=true
ENV NEW_RELIC_LICENSE_KEY=6564dfebeeeaa9bf25abf1aa0e8124ebFFFFNRAL
ENV NEW_RELIC_LOG_LEVEL=info
ENTRYPOINT [ "newrelic-admin", "run-program" ]