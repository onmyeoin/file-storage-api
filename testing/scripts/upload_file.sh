#!/bin/bash

# takes 2 args, filepath of file you wish to upload and metadata in JSON string format (use "{}" for no metadata)
# example metadata -  "{\"category\": \"personal\", \"subject\": \"me\", \"filetype\": \"jpg\"}"

log_file="../logs/test.log"

file_path=$1
metadata=$2


curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -u eoinoreilly:inscribe24 \
  -F "file=@${file_path}" \
  -F "metadata=${metadata}" \
  -w "\nResponse Code: %{http_code}\n" -o - >> "$log_file" 2>&1


echo "Logged on $(date)" >> "$log_file"