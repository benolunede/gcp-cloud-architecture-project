from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client()

project_id = client.project
dataset_id = "helsinki_tech_analytics"
table_id = "cloud_infrastructure_metrics"

# 1. Define a clean schema for cloud cost/performance logs
schema = [
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("service_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("cpu_utilization", "FLOAT", mode="REQUIRED"),
    bigquery.SchemaField("execution_cost_eur", "FLOAT", mode="REQUIRED"),
]

# 2. Create the Dataset if it doesn't exist
dataset_ref = bigquery.Dataset(f"{project_id}.{dataset_id}")
dataset_ref.location = "EU"
try:
    client.create_dataset(dataset_ref, exists_ok=True)
    print(f"Dataset {dataset_id} confirmed/created.")
except Exception as e:
    print(f"Error creating dataset: {e}")

# 3. Create the table explicitly with partition constraints (Crucial PCA skill)
table_ref = bigquery.Table(f"{project_id}.{dataset_id}.{table_id}", schema=schema)

# Optimize costs by partitioning the table by time automatically
table_ref.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="timestamp" 
)

try:
    client.create_table(table_ref, exists_ok=True)
    print(f"Partitioned table {table_id} ready.")
except Exception as e:
    print(f"Error creating table: {e}")

# 4. Generate mock operational data to insert
rows_to_insert = [
    {"timestamp": "2026-09-16T12:00:00Z", "service_name": "gke-cluster-prod", "cpu_utilization": 74.2, "execution_cost_eur": 12.50},
    {"timestamp": "2026-09-16T12:05:00Z", "service_name": "cloud-run-api", "cpu_utilization": 14.8, "execution_cost_eur": 0.02},
]

# Stream data straight into BigQuery
errors = client.insert_rows_json(f"{project_id}.{dataset_id}.{table_id}", rows_to_insert)
if not errors:
    print("Cloud operational metrics safely stored in BigQuery!")
else:
    print(f"Errors occurred during streaming ingestion: {errors}")
