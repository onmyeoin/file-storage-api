#!/bin/bash

# takes 2 args, fild_id that you want to retrieve and the destination to save file to 

log_file="../logs/test.log"

file_id=$1
file_path_to_save=$2

curl -X GET "http://localhost:8000/files/${file_id}" \
    -u eoinoreilly:inscribe24 \
    -o "${file_path_to_save}" \
    -w "\nResponse Code: %{http_code}\n" -o - >> "$log_file" 2>&1

echo "Logged on $(date)" >> "$log_file"