#!/bin/bash
function aws_sso_login() {
  local profile_name

  # Get the profile name from the user
  profile_name=$(list_aws_profiles | fzf)

  # If the user entered a profile name, log in to AWS using SSO
  if [[ -n "${profile_name}" ]]; then
    aws sso login --profile "${profile_name}"
    
    # Update kubeconfig for all EKS clusters associated with the selected profile
    update_all_eks_kubeconfig "${profile_name}"
    update_eks_docker "${profile_name}"
  fi
}

function update_all_eks_kubeconfig() {
  local profile_name="$1"
  local config_file="${HOME}/.aws/config"

  # Check if the config file exists and is readable
  if [[ ! -f "$config_file" || ! -r "$config_file" ]]; then
    echo "Config file not found or not readable: $config_file"
    return 1
  fi

  # Extract the cluster ARNs for the specified profile using AWS CLI and jq
  local cluster_arns=( $(aws eks list-clusters --profile "${profile_name}" --output json | jq -r '.clusters[]') )

  # Loop through each cluster ARN and update kubeconfig
  for cluster_arn in ${cluster_arns}; do
    cluster_name=$(basename "${cluster_arn}")
    echo "Updating kubeconfig for cluster: ${cluster_name}"
    aws eks update-kubeconfig --name "${cluster_name}" --profile "${profile_name}" --alias "${cluster_name}"
    echo "Kubeconfig updated for cluster: ${cluster_name}"
    echo
  done
}

function update_eks_docker() {
  local profile_name="$1"
  local config_file="${HOME}/.aws/config"

  # Check if the config file exists and is readable
  if [[ ! -f "$config_file" || ! -r "$config_file" ]]; then
    echo "Config file not found or not readable: $config_file"
    return 1
  fi

  local aws_account_id=$(aws configure get --profile "${profile_name}" sso_account_id)
  local region=$(aws configure get --profile "${profile_name}" region)
  local sso_role_name=$(aws configure get --profile "${profile_name}" sso_role_name)
  aws configure set sso_role_name AWSReadOnlyAccess --profile "${profile_name}"
  aws ecr get-login-password --profile "${profile_name}" | podman login --username AWS --password-stdin ${aws_account_id}.dkr.ecr.${region}.amazonaws.com
  aws configure set sso_role_name "${sso_role_name}" --profile "${profile_name}"
}

# Original list_aws_profiles function remains the same.
function list_aws_profiles() {
  local config_file="${HOME}/.aws/config"

  # Check if the config file exists and is readable
  if [[ ! -f "$config_file" || ! -r "$config_file" ]]; then
    echo "Config file not found or not readable: $config_file"
    return 1
  fi

  # Extract the profile names using grep and awk
  local profile_names=$(cat "$config_file" | grep profile | awk '{print $2}' | sed 's/]//g')

  # Print the profile names as a space-separated list
  echo "${profile_names[@]}"
}
