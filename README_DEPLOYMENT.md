# Quick Start: Cloud Run Deployment

## Summary

This microservice has been configured to:
- ✅ Connect to CloudSQL MySQL database
- ✅ Deploy to Google Cloud Run
- ✅ Use Unix socket connection for CloudSQL (Cloud Run native)
- ✅ Support local development with TCP connection

## Key Files Created

1. **`utils/database.py`** - Database connection configuration (CloudSQL + local)
2. **`models/db_models.py`** - SQLAlchemy database models
3. **`main.py`** - Updated to use database instead of in-memory storage
4. **`Dockerfile`** - Container image for Cloud Run
5. **`cloudbuild.yaml`** - Cloud Build configuration
6. **`DEPLOYMENT.md`** - Detailed deployment guide

## Quick Deployment Steps

1. **Create CloudSQL instance:**
   ```bash
   gcloud sql instances create matcha-db \
     --database-version=MYSQL_8_0 \
     --tier=db-f1-micro \
     --region=us-central1 \
     --root-password=cloudettes
   
   gcloud sql databases create matcha_db --instance=matcha-db
   ```

2. **Store password as secret:**
   ```bash
   echo -n "cloudettes" | gcloud secrets create db-password --data-file=-
   ```

3. **Deploy to Cloud Run:**
   ```bash
   export PROJECT_ID=$(gcloud config get-value project)
   export REGION=us-central1
   export INSTANCE_NAME=matcha-db
   
   gcloud run deploy matcha-api \
     --source . \
     --platform managed \
     --region $REGION \
     --allow-unauthenticated \
     --add-cloudsql-instances $PROJECT_ID:$REGION:$INSTANCE_NAME \
     --set-secrets DB_PASSWORD=db-password:latest \
     --set-env-vars \
       DB_NAME=matcha_db,\
       DB_USER=root,\
       CLOUD_SQL_CONNECTION_NAME=$PROJECT_ID:$REGION:$INSTANCE_NAME
   ```

## Environment Variables for Cloud Run

The service automatically detects CloudSQL when `CLOUD_SQL_CONNECTION_NAME` is set and uses Unix socket connection.

Required:
- `CLOUD_SQL_CONNECTION_NAME` - Format: `project:region:instance`
- `DB_PASSWORD` - From Secret Manager
- `DB_NAME` - Database name (default: `matcha_db`)
- `DB_USER` - Database user (default: `root`)

## Local Development

For local testing with CloudSQL Proxy:

```bash
# Start Cloud SQL Proxy
./cloud-sql-proxy $PROJECT_ID:$REGION:$INSTANCE_NAME

# Set environment variables
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=YOUR_PASSWORD
export DB_NAME=matcha_db

# Run the app
python main.py
```

## Database Schema

Tables are automatically created on first startup via `init_db()`. The schema includes:

- **users** table - User profiles with relationships to matcha sessions
- **matcha_sessions** table - Matcha drinking session records

See `models/db_models.py` for full schema details.

## Testing

After deployment, test the API:

```bash
export SERVICE_URL=$(gcloud run services describe matcha-api \
  --region=us-central1 --format='value(status.url)')

curl $SERVICE_URL/health
curl $SERVICE_URL/docs  # OpenAPI documentation
```

For detailed deployment instructions, see `DEPLOYMENT.md`.

