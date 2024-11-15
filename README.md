# File Storage API

This API allows users to upload, retrieve, search, and delete PDF and image files with associated metadata. Files are stored on disk, while metadata and file paths are managed in a PostgreSQL database. The setup also includes example testing scripts and a logging system to track test actions.

## Project Structure

- `file_storage_api/`
    - `files/`
    - `testing/`
        - `input/`: Contains sample files for upload.
        - `output/`: Store retrieved files here.
        - `scripts/`: Contains executable test scripts to interact with the API. (Intructions for each can be found in the scripts themselves)
            - `delete_file.sh` 
            - `retrieve_by_metadata.sh` 
            - `retrieve_file.sh` 
            - `upload_file.sh` 
        - `logs/`: Contains a log file for test script executions.
            - `test.log`
    - `database.py`
    - `docker-compose.yml`
    - `Dockerfile`
    - `main.py`
    - `models.py`
    - `requirements.txt`


## Requirements

- **Docker** and **Docker Compose**: The application runs in a containerized environment.
- **FastAPI**, **SQLAlchemy**, **PostgreSQL** (handled by Docker Compose).

## Setup Instructions

1. Start the application using Docker Compose:
   ```bash 
   docker-compose up --build
   ```

   This command builds and starts the FastAPI application with PostgreSQL, exposing the API on `http://localhost:8000`.

## Using the API

Please note: Some test scripts are available in the testing directory with some test files for input.

Alternatively the below templates can be used to run your own commands.

### 1. Upload a File
   - **Endpoint**: `POST /upload`
   - **Description**: Upload a file with associated metadata.
   - **Example**:
     ```bash
     curl -X POST "http://localhost:8000/upload" \
       -H "Content-Type: multipart/form-data" \
       -F "file=@input/sample.pdf" \
       -F "metadata={\"category\": \"inscribe\", \"subject\": \"technical\"}"
     ```

### 2. Retrieve a File by ID
   - **Endpoint**: `GET /files/{file_id}`
   - **Description**: Retrieves a file by its unique ID, storing it in the `output` directory.
   - **Example**:
     ```bash
     curl -X GET "http://localhost:8000/files/1" -o ../output/retrieved_file.pdf
     ```

### 3. Search Files by Metadata
   - **Endpoint**: `GET /files`
   - **Description**: Searches for files matching specified metadata and store as zip folder (if multiple files returned)
   - **Example**:
     ```bash
     curl -G "http://localhost:8000/files" --data-urlencode "category=document" --data-urlencode "subject=banking" -o ../output/matched_files.zip
     ```

### 4. Delete a File
   - **Endpoint**: `DELETE /files/{file_id}`
   - **Description**: Deletes a file by its unique ID.
   - **Example**:
     ```bash
     curl -X DELETE "http://localhost:8000/files/1"
     ```

## Testing Scripts

Located in `testing/scripts/`, these scripts provide an easy way to interact with the API. Details on usage are included within each script. Here’s a summary:

- **`upload.sh`**: 
    - Uploads file.  
    - Takes 2 args, filepath and metadata. 
    - metadata should be a JSON string eg "{\"category\": \"personal\", \"subject\": \"me\", \"filetype\": \"jpg\"}"
- **`retrieve_file.sh`**: 
    - Retrieves a file by its unique ID.
    - Takes 2 args, file_id and filepath to save file to (filepath must also specify destination filename)
- **`retrieve_by_metadata.sh`**: 
    - Searches for files by metadata and saves results in `output`.
    - Takes no args, curl command in script must be updated for metadata you wish to filter by
- **`delete_file.sh`**: 
    - Deletes a file by its unique ID.
    - Takes 1 arg, file_id you wish to delete 

Each script logs its actions to `logs/upload_log.txt`, including response codes and timestamps.

## Logs

All interactions during testing are logged in `testing/logs/upload_log.txt`. This log file includes:

- Each action performed by the scripts
- Timestamps for each action
- HTTP response codes for uploads, retrievals, and deletions