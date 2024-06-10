#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 bucket-name"
    exit 1
fi

BUCKET_NAME=$1

echo "Deleting all versions and delete markers from bucket: $BUCKET_NAME"

# Function to delete all versions
delete_all_versions() {
    versions=$(aws s3api list-object-versions --bucket $BUCKET_NAME)
    while [[ $(echo $versions | jq -r '.Versions | length') -gt 0 ]]; do
        for version in $(echo $versions | jq -r '.Versions[] | @base64'); do
            _jq() {
                echo ${version} | base64 --decode | jq -r ${1}
            }
            key=$(_jq '.Key')
            versionId=$(_jq '.VersionId')
            aws s3api delete-object --bucket $BUCKET_NAME --key "$key" --version-id "$versionId"
        done
        versions=$(aws s3api list-object-versions --bucket $BUCKET_NAME)
    done
}

# Function to delete all delete markers
delete_all_markers() {
    markers=$(aws s3api list-object-versions --bucket $BUCKET_NAME)
    while [[ $(echo $markers | jq -r '.DeleteMarkers | length') -gt 0 ]]; do
        for marker in $(echo $markers | jq -r '.DeleteMarkers[] | @base64'); do
            _jq() {
                echo ${marker} | base64 --decode | jq -r ${1}
            }
            key=$(_jq '.Key')
            versionId=$(_jq '.VersionId')
            aws s3api delete-object --bucket $BUCKET_NAME --key "$key" --version-id "$versionId"
        done
        markers=$(aws s3api list-object-versions --bucket $BUCKET_NAME)
    done
}

# Delete all versions and markers
delete_all_versions
delete_all_markers

# Finally, delete the bucket
echo "Deleting the bucket: $BUCKET_NAME"
aws s3 rb s3://$BUCKET_NAME --force

echo "Bucket $BUCKET_NAME and all its versions have been deleted."
