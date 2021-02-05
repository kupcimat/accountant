#!/bin/sh

# Create S3 buckets
awslocal s3 mb s3://accountant-document-uploads
awslocal s3 mb s3://accountant-document-results

# Create SQS queue
awslocal sqs create-queue \
  --queue-name accountant-worker-queue \
  --attributes ReceiveMessageWaitTimeSeconds=10,VisibilityTimeout=30

# Add S3 bucket notification
awslocal s3api put-bucket-notification-configuration \
  --bucket accountant-document-uploads \
  --notification-configuration file:///docker-entrypoint-initaws.d/s3-notification.json
