#!/bin/bash
# Deployment script for Cloud Run

export PROJECT_ID=microservice-1-479117
export REGION=us-central1
export INSTANCE_NAME=matcha-db

./google-cloud-sdk/bin/gcloud run deploy matcha-api \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $PROJECT_ID:$REGION:$INSTANCE_NAME \
  --set-secrets DB_PASSWORD=db-password:latest \
  --set-env-vars DB_NAME=matcha_db,DB_USER=root,CLOUD_SQL_CONNECTION_NAME=$PROJECT_ID:$REGION:$INSTANCE_NAME

