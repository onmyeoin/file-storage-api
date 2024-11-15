#!/bin/bash

log_file="../logs/test.log"

# takes 1 arg, file_id you wish to delete

file_id=$1
curl -X DELETE "http://localhost:8000/files/${file_id}" -u eoinoreilly:inscribe24 -w "\nResponse Code: %{http_code}\n" -o - >> "$log_file" 2>&1
echo "Logged on $(date)" >> "$log_file"
