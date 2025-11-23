#!/bin/bash
# Deploy using Cloud Build to avoid ZIP timestamp issues

echo "Submitting build to Cloud Build (this will build and deploy automatically)..."
~/Downloads/google-cloud-sdk/bin/gcloud builds submit --config=cloudbuild-simple.yaml

echo "Deployment complete!"

