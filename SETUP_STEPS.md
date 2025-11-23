# Step-by-Step Setup Guide

## Prerequisites Checklist

Before running the deployment commands, you need:

- [ ] **Google Cloud Account** - Sign up at https://cloud.google.com (free trial available)
- [ ] **Google Cloud Project** - Create one at https://console.cloud.google.com
- [ ] **gcloud CLI installed** - Install from https://cloud.google.com/sdk/docs/install
- [ ] **Billing enabled** - Required for CloudSQL (but free tier available)

## Step 0: Install and Setup gcloud CLI

### On macOS:
```bash
# Download and install
curl https://sdk.cloud.google.com | bash

# Restart your shell or run:
exec -l $SHELL

# Initialize gcloud
gcloud init
```

During `gcloud init`, you'll:
1. Login to your Google account
2. Select or create a project
3. Choose a default region

### Verify installation:
```bash
gcloud --version
gcloud config list
```

## Step 1: Enable Required APIs

Before creating resources, enable the necessary APIs:

```bash
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com
```

## Step 2: Create CloudSQL Instance

**Note:** The command creates the instance automatically - you don't need to create it in the web console!

```bash
gcloud sql instances create matcha-db \
  --database-version=MYSQL_8_0 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --root-password=cloudettes
```

This will take 5-10 minutes. You'll see output like:
```
Creating Cloud SQL instance...done.
Created [https://sqladmin.googleapis.com/...].
```

Then create the database:
```bash
gcloud sql databases create matcha_db --instance=matcha-db
```

## Step 3: Store Password as Secret

```bash
echo -n "cloudettes" | gcloud secrets create db-password --data-file=-
```

## Step 4: Deploy to Cloud Run

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

This will:
1. Build your Docker image
2. Push it to Container Registry
3. Deploy to Cloud Run
4. Connect to your CloudSQL instance

## Step 5: Grant Secret Access (if needed)

If you get permission errors, grant access:

```bash
export SERVICE_ACCOUNT=$(gcloud run services describe matcha-api \
    --region=$REGION \
    --format='value(spec.template.spec.serviceAccountName)')

gcloud secrets add-iam-policy-binding db-password \
    --member="serviceAccount:$SERVICE_ACCOUNT" \
    --role="roles/secretmanager.secretAccessor"
```

## Step 6: Test the Deployment

```bash
export SERVICE_URL=$(gcloud run services describe matcha-api \
  --region=us-central1 --format='value(status.url)')

curl $SERVICE_URL/health
curl $SERVICE_URL/docs  # OpenAPI documentation
```

## Troubleshooting

### If gcloud command not found:
- Make sure you've installed it and restarted your terminal
- On macOS, you may need to add to PATH: `export PATH=$PATH:/usr/local/bin`

### If "project not found":
- Run `gcloud projects list` to see available projects
- Set project: `gcloud config set project YOUR_PROJECT_ID`

### If "billing not enabled":
- Go to https://console.cloud.google.com/billing
- Link a billing account to your project

### If CloudSQL creation fails:
- Check you have billing enabled
- Verify the region is available: `gcloud sql regions list`
- Try a different region if needed

