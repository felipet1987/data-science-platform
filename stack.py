import pulumi
from pulumi_command import local
import os

# This Pulumi stack is now designed for a single Ubuntu VM (cloud or on-premises).
# It provisions a docker-compose.yaml file and can optionally run Docker Compose to launch all services.

# Write the docker-compose.yaml file for the Open Data Stack
compose_content = '''
version: '3.8'
services:
  postgres:
    image: postgres:15
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: adminpassword
      POSTGRES_DB: data_science
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  minio:
    image: minio/minio:latest
    command: server /data
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio-data:/data

  metabase:
    image: metabase/metabase:latest
    ports:
      - "3000:3000"
    depends_on:
      - postgres

  superset:
    image: apache/superset:latest
    environment:
      SUPERSET_SECRET_KEY: supersetsecret
    ports:
      - "8088:8088"
    depends_on:
      - postgres

  airflow:
    image: apache/airflow:2.8.1
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__FERNET_KEY: "fernetkey"
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://admin:adminpassword@postgres/data_science
      AIRFLOW__WEBSERVER__SECRET_KEY: "airflowsecret"
    ports:
      - "8080:8080"
    depends_on:
      - postgres
    command: bash -c "airflow db upgrade && airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@example.com && airflow webserver"

  meltano:
    image: meltano/meltano:latest
    command: ui
    ports:
      - "5000:5000"

  dbt:
    image: ghcr.io/dbt-labs/dbt-postgres:1.7.8
    entrypoint: ["tail", "-f", "/dev/null"] # Placeholder, run dbt manually

  duckdb:
    image: duckdb/duckdb:latest
    entrypoint: ["tail", "-f", "/dev/null"] # Placeholder, run duckdb manually

  spark:
    image: bitnami/spark:latest
    environment:
      SPARK_MODE: master
    ports:
      - "7077:7077"
      - "8081:8081"

volumes:
  pgdata:
  minio-data:
'''

compose_file = local.Command(
    "write-docker-compose",
    create=f"echo '{compose_content}' > docker-compose.yaml",
    opts=pulumi.ResourceOptions(replace_on_changes=["create"]),
)

# Optionally, run Docker Compose to bring up the stack
deploy_stack = local.Command(
    "docker-compose-up",
    create="docker-compose up -d",
    opts=pulumi.ResourceOptions(depends_on=[compose_file]),
)

# Export service endpoints (assuming direct VM ports)
pulumi.export("postgres_url", pulumi.Output.secret("postgresql://admin:adminpassword@localhost:5432/data_science"))
pulumi.export("minio_url", pulumi.Output.secret("http://localhost:9000"))
pulumi.export("metabase_url", pulumi.Output.secret("http://localhost:3000"))
pulumi.export("superset_url", pulumi.Output.secret("http://localhost:8088"))
pulumi.export("airflow_url", pulumi.Output.secret("http://localhost:8080"))
pulumi.export("meltano_url", pulumi.Output.secret("http://localhost:5000"))
pulumi.export("spark_master_url", pulumi.Output.secret("http://localhost:8081"))

# Notes:
# - You must have Docker and Docker Compose installed on your Ubuntu VM.
# - This stack will overwrite docker-compose.yaml in the project directory.
# - You can run `pulumi up` to deploy and manage the stack.
# - For production, secure passwords, use HTTPS, and configure firewalls appropriately.
