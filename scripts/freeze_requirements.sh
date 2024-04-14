#!/bin/bash

# Define your requirement files here
declare -a files=("requirements.txt")

for file in "${files[@]}"; do
  
  # Extract the base filename without extension
  filename=$(basename "$file" .txt)
  env_name="venv_${filename}"
  
  echo "Processing $file..."
  python -m venv "$env_name"
  
  source "$env_name/bin/activate"
  pip install --upgrade pip
  pip install -r "$file"
  pip freeze > "${filename}-freeze.txt"
  deactivate
  
  rm -rf "$env_name"
  echo "$file processed. Output: ${filename}-freeze.txt"
done

echo "Freeze requirements done."
