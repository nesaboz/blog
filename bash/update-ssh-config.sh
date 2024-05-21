#!/bin/zsh

# Path to SSH configuration file
SSH_CONFIG="$HOME/.ssh/config"
TEMP_CONFIG=$(mktemp)

# Fetch instance details using AWS CLI
instance_data=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId, Tags[?Key==`Name`].Value | [0], PublicIpAddress]' --output text)

# Backup the original SSH config file
cp "$SSH_CONFIG" "$SSH_CONFIG.bak"

# Create an associative array to store instance names and IPs
typeset -A aws_instances

# Read instance details into the associative array
while read -r instance_id name public_ip; do
    if [[ -n $public_ip && -n $name ]]; then
        aws_instances[$name]=$public_ip
    fi
done <<< "$instance_data"

# Function to remove AWS instance entries
# Function to remove AWS instance entries
filter_aws_entries() {
    awk -v aws_hosts="$1" '
    BEGIN {
        # Split the aws_hosts string into an array of host names
        split(aws_hosts, hosts, " ")
        for (i in hosts) {
            aws[hosts[i]] = 1  # Mark these hosts in an associative array
        }
        inside_aws_block = 0  # Initialize a flag to track inside an AWS block
    }
    /^Host / {  # If the line starts with "Host "
        if (inside_aws_block) {
            inside_aws_block = 0  # End of an AWS block
        }
        if ($2 in aws) {  # Check if the host name is in the AWS array
            inside_aws_block = 1  # Start of an AWS block
            next  # Skip this line
        }
    }
    !inside_aws_block { print }  # Print lines that are not inside an AWS block
    ' "$2"
}

# Extract the names of AWS instances
aws_instance_names=$(echo "${(@k)aws_instances}" | tr ' ' '\n' | xargs)

# Filter out existing AWS entries and save to the temporary file
filter_aws_entries "$aws_instance_names" "$SSH_CONFIG" > "$TEMP_CONFIG"

# Append new AWS instance entries to the temporary SSH config file
for name in "${(@k)aws_instances}"; do
    public_ip=${aws_instances[$name]}
    # Prepare SSH config entry
    entry="Host $name
    HostName $public_ip
    User ubuntu
    IdentityFile ~/.ssh/my-aws-key.pem
"

    # Add new entry
    echo "$entry" >> "$TEMP_CONFIG"
done

# Ensure no extra newlines at the end of the temp file
sed -i '' -e '$a\' "$TEMP_CONFIG"

# Replace the original SSH config file with the updated one
mv "$TEMP_CONFIG" "$SSH_CONFIG"

echo "SSH config has been updated. Backup created at $SSH_CONFIG.bak"
