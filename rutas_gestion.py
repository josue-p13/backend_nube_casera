import os
import shutil
import urllib.parse
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()

extensiones_img = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

class FolderCreate(BaseModel):
    folder_name: str

def retorno_path(opcion):
    match opcion:
        case "vero":
            return "E:/Mami"
        case "josue":
            return "C:/Users/josue/Pictures/Screenshots"
        case "alejandro":
            return "C:/Users/josue/Pictures/Feedback"
        case _:
            raise HTTPException(status_code=404, detail="User path not found")

@router.post("/create_folder/{user}")
async def create_folder(user: str, folder_data: FolderCreate, subpath: str = ''):
    try:
        base_path = retorno_path(user)
    except HTTPException as e:
        raise e

    decoded_subpath = urllib.parse.unquote(subpath)
    current_path_relative = os.path.normpath(decoded_subpath)
    if os.path.isabs(current_path_relative) or ".." in current_path_relative.split(os.path.sep):
        current_path_relative = ''

    target_full_path = os.path.normpath(os.path.join(base_path, current_path_relative))

    if not target_full_path.startswith(os.path.normpath(base_path)):
        raise HTTPException(status_code=403, detail="Access forbidden")

    new_folder_name = folder_data.folder_name.strip()
    if not new_folder_name or ".." in new_folder_name or "/" in new_folder_name or "\\" in new_folder_name:
        raise HTTPException(status_code=400, detail="Invalid folder name")

    new_folder_path = os.path.join(target_full_path, new_folder_name)

    try:
        os.makedirs(new_folder_path, exist_ok=False)
        return JSONResponse(content={"message": f"Folder '{new_folder_name}' created successfully"}, status_code=201)
    except FileExistsError:
        raise HTTPException(status_code=409, detail=f"Folder '{new_folder_name}' already exists")
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Error creating folder: {e}")

@router.post("/upload/{user}")
async def upload_file(user: str, subpath: str = Form(''), file: UploadFile = File(...)):
    try:
        base_path = retorno_path(user)
    except HTTPException as e:
        raise e

    decoded_subpath = urllib.parse.unquote(subpath)
    current_path_relative = os.path.normpath(decoded_subpath)
    if os.path.isabs(current_path_relative) or ".." in current_path_relative.split(os.path.sep):
        current_path_relative = ''

    upload_folder_path = os.path.normpath(os.path.join(base_path, current_path_relative))

    if not upload_folder_path.startswith(os.path.normpath(base_path)):
        raise HTTPException(status_code=403, detail="Access forbidden")

    if not os.path.exists(upload_folder_path) or not os.path.isdir(upload_folder_path):
        raise HTTPException(status_code=404, detail="Upload directory not found")

    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()
    if extension not in extensiones_img:
        raise HTTPException(status_code=400, detail=f"File type '{extension}' not allowed. Allowed: {', '.join(extensiones_img)}")

    file_location = os.path.join(upload_folder_path, filename)

    if os.path.exists(file_location):
        raise HTTPException(status_code=409, detail=f"File '{filename}' already exists.")

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=f"Could not upload file: {e}")
    finally:
        file.file.close()

    return JSONResponse(content={"message": f"File '{filename}' uploaded successfully to '{current_path_relative}'"}, status_code=201)