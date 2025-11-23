#!/bin/bash
# Fixed deployment script that builds Docker image first to avoid ZIP timestamp issues

export PROJECT_ID=microservice-1-479117
export REGION=us-central1
export INSTANCE_NAME=matcha-db
export IMAGE_NAME=gcr.io/$PROJECT_ID/matcha-api:latest

echo "Building Docker image..."
./google-cloud-sdk/bin/docker build -t $IMAGE_NAME .

echo "Pushing Docker image to Container Registry..."
./google-cloud-sdk/bin/docker push $IMAGE_NAME

echo "Deploying to Cloud Run..."
./google-cloud-sdk/bin/gcloud run deploy matcha-api \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances $PROJECT_ID:$REGION:$INSTANCE_NAME \
  --set-secrets DB_PASSWORD=db-password:latest \
  --set-env-vars DB_NAME=matcha_db,DB_USER=root,CLOUD_SQL_CONNECTION_NAME=$PROJECT_ID:$REGION:$INSTANCE_NAME

echo "Deployment complete!"

