#!/usr/bin/env bash
export BUCKET_NAME=paparazzi-screenshots
awslocal s3api create-bucket --bucket ${BUCKET_NAME} --region ap-south-1 --create-bucket-configuration LocationConstraint=ap-south-1

