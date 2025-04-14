import os
import urllib.parse
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse

router = APIRouter()

extensiones_img = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

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

@router.get("/browse")
async def browse_directory(user: str, subpath: str = ''):
    try:
        base_path = retorno_path(user)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    # Asegurar que subpath es una cadena vacía si es None
    if subpath is None:
        subpath = ''
        
    decoded_subpath = urllib.parse.unquote(subpath)
    current_path_relative = os.path.normpath(decoded_subpath)
    if os.path.isabs(current_path_relative) or ".." in current_path_relative.split(os.path.sep):
        current_path_relative = ''

    current_full_path = os.path.join(base_path, current_path_relative)
    current_full_path = os.path.normpath(current_full_path)

    if not current_full_path.startswith(os.path.normpath(base_path)):
        return JSONResponse(status_code=403, content={"detail": "Access forbidden"})

    if not os.path.exists(current_full_path) or not os.path.isdir(current_full_path):
        return JSONResponse(status_code=404, content={"detail": "Directory not found"})

    items = []
    try:
        for item_name in os.listdir(current_full_path):
            item_full_path = os.path.join(current_full_path, item_name)
            item_relative_to_base = os.path.relpath(item_full_path, base_path)
            item_url_path = item_relative_to_base.replace("\\", "/")

            if os.path.isdir(item_full_path):
                items.append({"type": "directory", "name": item_name, "path": item_url_path})
            elif os.path.isfile(item_full_path):
                extension = os.path.splitext(item_name)[1].lower()
                if extension in extensiones_img:
                    encoded_url_path = urllib.parse.quote(item_url_path)
                    file_url = f"/media/{user}/{encoded_url_path}"
                    items.append({"type": "file", "name": item_name, "url": file_url})
    except OSError as e:
        return JSONResponse(status_code=500, content={"detail": f"Error reading directory: {e}"})

    parent_path = os.path.dirname(current_path_relative) if current_path_relative else None
    if parent_path is not None:
        parent_path = parent_path.replace("\\", "/")
        if parent_path == ".":
            parent_path = ""

    return JSONResponse(content={
        "currentPath": current_path_relative.replace("\\", "/"),
        "parentPath": parent_path,
        "items": items
    })

@router.get("/media/{user}/{file_path:path}")
async def get_media_file(user: str, file_path: str):
    try:
        base_path = retorno_path(user)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    decoded_file_path = urllib.parse.unquote(file_path)
    if ".." in decoded_file_path.split(os.path.sep):
        raise HTTPException(status_code=403, detail="Access forbidden")

    full_file_path = os.path.normpath(os.path.join(base_path, decoded_file_path))

    if not full_file_path.startswith(os.path.normpath(base_path)):
        raise HTTPException(status_code=403, detail="Access forbidden")

    if not os.path.isfile(full_file_path):
        raise HTTPException(status_code=404, detail="File not found")

    extension = os.path.splitext(full_file_path)[1].lower()
    if extension not in extensiones_img:
        raise HTTPException(status_code=403, detail="File type not allowed")

    return FileResponse(full_file_path)