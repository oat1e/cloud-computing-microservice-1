# Cloud Run Deployment Guide

This guide explains how to deploy the Matcha Drinking Tracker API to Google Cloud Run with CloudSQL.

## Prerequisites

1. Google Cloud Project with billing enabled
2. `gcloud` CLI installed and authenticated
3. CloudSQL MySQL instance created
4. Docker installed (for local testing)

## Step 1: Create CloudSQL MySQL Instance

```bash
# Set your project ID
export PROJECT_ID=your-project-id
export REGION=us-central1
export INSTANCE_NAME=matcha-db

# Create CloudSQL MySQL instance
gcloud sql instances create $INSTANCE_NAME \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=$REGION \
    --root-password=YOUR_ROOT_PASSWORD

# Create database
gcloud sql databases create matcha_db --instance=$INSTANCE_NAME

# Create a user (optional, or use root)
gcloud sql users create dbuser \
    --instance=$INSTANCE_NAME \
    --password=YOUR_USER_PASSWORD
```

## Step 2: Store Database Password as Secret

```bash
# Create a secret for the database password
echo -n "YOUR_DB_PASSWORD" | gcloud secrets create db-password \
    --data-file=- \
    --replication-policy="automatic"
```

## Step 3: Enable Required APIs

```bash
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com
```

## Step 4: Build and Deploy

### Option A: Using Cloud Build (Recommended)

1. Update `cloudbuild.yaml` with your CloudSQL instance connection name:
   ```yaml
   substitutions:
     _CLOUD_SQL_INSTANCE: 'PROJECT_ID:REGION:INSTANCE_NAME'
   ```

2. Submit the build:
   ```bash
   gcloud builds submit --config=cloudbuild.yaml
   ```

### Option B: Manual Deployment

1. Build the Docker image:
   ```bash
   docker build -t gcr.io/$PROJECT_ID/matcha-api:latest .
   ```

2. Push to Container Registry:
   ```bash
   docker push gcr.io/$PROJECT_ID/matcha-api:latest
   ```

3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy matcha-api \
     --image gcr.io/$PROJECT_ID/matcha-api:latest \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --add-cloudsql-instances $PROJECT_ID:$REGION:$INSTANCE_NAME \
     --set-secrets DB_PASSWORD=db-password:latest \
     --set-env-vars \
       DB_NAME=matcha_db,\
       DB_USER=root,\
       CLOUD_SQL_CONNECTION_NAME=$PROJECT_ID:$REGION:$INSTANCE_NAME
   ```

## Step 5: Grant Permissions

Ensure Cloud Run service account has access to the secret:

```bash
export SERVICE_ACCOUNT=$(gcloud run services describe matcha-api \
    --region=$REGION \
    --format='value(spec.template.spec.serviceAccountName)')

gcloud secrets add-iam-policy-binding db-password \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"
```

## Step 6: Initialize Database Tables

The application will automatically create tables on first startup. Alternatively, you can run migrations manually:

```bash
# Connect to CloudSQL instance
gcloud sql connect $INSTANCE_NAME --user=root

# Or use Cloud SQL Proxy for local connection
```

## Environment Variables

The application uses the following environment variables:

- `PORT`: Port to listen on (default: 8080, Cloud Run sets this automatically)
- `DB_HOST`: Database host (not needed for Cloud Run with Unix socket)
- `DB_PORT`: Database port (not needed for Cloud Run with Unix socket)
- `DB_USER`: Database user (default: root)
- `DB_PASSWORD`: Database password (from secret)
- `DB_NAME`: Database name (default: matcha_db)
- `CLOUD_SQL_CONNECTION_NAME`: CloudSQL connection name (format: project:region:instance)
- `DB_SOCKET_DIR`: Unix socket directory (default: /cloudsql)

## Local Development with CloudSQL

To connect locally to CloudSQL:

1. Install Cloud SQL Proxy:
   ```bash
   curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.8.0/cloud-sql-proxy.linux.amd64
   chmod +x cloud-sql-proxy
   ```

2. Run the proxy:
   ```bash
   ./cloud-sql-proxy $PROJECT_ID:$REGION:$INSTANCE_NAME
   ```

3. Set environment variables:
   ```bash
   export DB_HOST=127.0.0.1
   export DB_PORT=3306
   export DB_USER=root
   export DB_PASSWORD=YOUR_PASSWORD
   export DB_NAME=matcha_db
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Testing the Deployment

Once deployed, test the API:

```bash
# Get the service URL
export SERVICE_URL=$(gcloud run services describe matcha-api \
    --region=$REGION \
    --format='value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health

# Test creating a user
curl -X POST $SERVICE_URL/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }'
```

## Troubleshooting

### Connection Issues

- Verify CloudSQL instance is running: `gcloud sql instances describe $INSTANCE_NAME`
- Check Cloud Run logs: `gcloud run services logs read matcha-api --region=$REGION`
- Ensure CloudSQL connection name is correct format: `project:region:instance`

### Permission Issues

- Verify service account has CloudSQL Client role
- Check secret access permissions
- Ensure Cloud Run service has access to CloudSQL instance

### Database Issues

- Check database exists: `gcloud sql databases list --instance=$INSTANCE_NAME`
- Verify user credentials
- Check firewall rules if connecting from outside Cloud Run

## Cost Optimization

- Use `db-f1-micro` tier for development
- Set minimum instances to 0 for cost savings (cold starts acceptable)
- Use Cloud SQL Proxy connection pooling for production

## Security Best Practices

1. Use Secret Manager for sensitive data (passwords, API keys)
2. Enable SSL/TLS for database connections
3. Use least privilege IAM roles
4. Enable VPC connector for private IP if needed
5. Regularly rotate database passwords

