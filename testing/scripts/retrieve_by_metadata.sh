#!/bin/bash

# this is for testing purposes 

# change metadata to fit the metadata you wish to filter on

log_file="../logs/test.log"

curl -G "http://localhost:8000/files" --data-urlencode "category=Dogs" --data-urlencode "subject=Otis" -o ../output/Otis.zip \
    -w "\nResponse Code: %{http_code}\n" -o - >> "$log_file" 2>&1

echo "Logged on $(date)" >> "$log_file"


