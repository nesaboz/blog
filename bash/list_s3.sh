#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 bucket-name"
    exit 1
fi

BUCKET_NAME=$1

echo $BUCKET_NAME
