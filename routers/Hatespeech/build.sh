#!/bin/sh

region="us-east-1"
aws_account_id="998363457537"
project_name="hatespeech"

echo "Building docker image ... "
docker-compose build

echo "Getting login password"
aws ecr get-login-password  --region $region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$region.amazonaws.com

echo "Creating repository..."
aws ecr create-repository --repository-name $project_name

echo "logout now..."
docker logout

echo "Creating tags..."
docker tag $project_name:latest $aws_account_id.dkr.ecr.$region.amazonaws.com/$project_name

echo "login again..."
aws ecr get-login-password  --region $region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$region.amazonaws.com

echo "Pushing image..."
docker-compose push