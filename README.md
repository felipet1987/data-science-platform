# Data Science Platform: Single-VM Docker Compose Edition

This project sets up a complete open-source data science platform on a single Ubuntu VM using Docker Compose. All components run as containers and are orchestrated by Pulumi.

## Components Deployed

- PostgreSQL (database)
- MinIO (S3-compatible object storage)
- Metabase (BI/analytics dashboard)
- Superset (BI/analytics dashboard)
- Airflow (workflow scheduler)
- Meltano (data ingestion)
- dbt (data transformation)
- DuckDB (analytical database)
- Spark (big data compute)

## Prerequisites

- Python 3.8+
- Pulumi CLI
- Docker & Docker Compose installed on your Ubuntu VM
- (Optional) Virtualenv for Python dependencies

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Log in to Pulumi:
    ```bash
    pulumi login
    ```
3. Deploy the stack:
    ```bash
    pulumi up
    ```

This will generate a `docker-compose.yaml` and launch all services.

## Accessing Services

- PostgreSQL:      `localhost:5432` (user: admin, password: adminpassword)
- MinIO:           `http://localhost:9000` (user: minioadmin, password: minioadmin)
- Metabase:        `http://localhost:3000`
- Superset:        `http://localhost:8088`
- Airflow:         `http://localhost:8080`
- Meltano:         `http://localhost:5000`
- Spark Master UI: `http://localhost:8081`

## Notes
- All data is persisted in Docker volumes.
- For production, change all default passwords and configure firewalls.
- You can manage containers with Docker Compose directly:
    ```bash
    docker-compose ps
    docker-compose logs
    docker-compose down
    ```
- To update the stack, edit `stack.py` and run `pulumi up` again.

---

This setup is ideal for local development, prototyping, or small-scale deployments. For distributed/cloud setups, see the AWS/Kubernetes version.
```

3. Create a new stack:
```bash
pulumi stack init dev
```

4. Configure AWS credentials:
```bash
pulumi config set aws:region us-east-1
pulumi config set aws:profile your-profile
```

## Deployment

Deploy the infrastructure:
```bash
pulumi up
```

## Components

- **EKS Cluster**: Managed Kubernetes cluster for running data science workloads
- **S3 Bucket**: Secure storage for datasets and artifacts
- **RDS PostgreSQL**: Database for data science applications
- **ECR Repository**: Container registry for ML models and notebooks
- **IAM Roles**: Security policies for accessing resources

## Outputs

After deployment, the following outputs will be available:
- `postgres_url`: PostgreSQL connection string
- `minio_url`: MinIO S3-compatible object storage URL
- `metabase_url`: Metabase analytics dashboard
- `superset_url`: Superset analytics dashboard
- `airflow_url`: Airflow web UI
- `meltano_url`: Meltano UI
- `spark_master_url`: Spark Master UI

See above for default ports, credentials, and how to access each service.
