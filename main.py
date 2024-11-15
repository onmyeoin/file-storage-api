import os
import json
import uuid
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import File as FileModel
from sqlalchemy.exc import ProgrammingError
import zipfile
from io import BytesIO

app = FastAPI()

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

# Ensure the file storage directory exists
os.makedirs("files", exist_ok=True)

# Endpoint to upload a file
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    metadata: str = Form(...), 
    db: Session = Depends(get_db)
):
    # Ensure file is pdf, jpg or png 
    if file.content_type not in ["application/pdf", "image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Parse JSON string into dict 
    try:
        metadata_dict = json.loads(metadata)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format for metadata")

    # Save file with a unique ID - this is to prevent any accidental overlap with file names
    # File will be saved in the files directory - in production a proper file storage system such as AWS S3 or Azure blob storage would be better
    file_id = str(uuid.uuid4())
    file_path = f"files/{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # Save file metadata and file url in database
    db_file = FileModel(
        filename=file.filename,
        file_path=file_path,
        file_metadata=metadata_dict 
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return {"file_id": db_file.id, "filename": db_file.filename, "metadata": db_file.file_metadata}

# Endpoint to retrieve a file by ID
@app.get("/files/{file_id}")
async def get_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file or not os.path.exists(db_file.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(db_file.file_path)

# Endpoint to delete a file
@app.delete("/files/{file_id}")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Remove file from disk and delete record from database
    if os.path.exists(db_file.file_path):
        os.remove(db_file.file_path)
    db.delete(db_file)
    db.commit()
    return {"status": "File deleted"}

# endpoint to retrieve files by querying metadata
@app.get("/files")
async def search_files(request: Request, db: Session = Depends(get_db)):
    
    query = db.query(FileModel)

    # Iterate over each query parameter to dynamically build filters
    for key, value in request.query_params.items():
        try:
            query = query.filter(FileModel.file_metadata[key].astext == value)
        except ProgrammingError:
            raise HTTPException(status_code=400, detail=f"Invalid metadata key: '{key}'")

    files = query.all()
    if not files:
        raise HTTPException(status_code=404, detail="No files match the criteria")

    # If only one file matches, return it directly
    if len(files) == 1:
        file = files[0]
        if not os.path.exists(file.file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file.file_path, filename=file.filename)

    # If multiple files match, create a ZIP archive
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for file in files:
            if os.path.exists(file.file_path):
                zip_file.write(file.file_path, arcname=file.filename)
    
    zip_buffer.seek(0)

    # Return the ZIP archive
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=matched_files.zip"})

