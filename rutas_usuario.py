from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from buscar_base import buscar

router = APIRouter()

class Usuario(BaseModel):
    user: str
    password: str

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

@router.post("/tomar_datos/")
async def recibir_datos(usuario: Usuario):
    print(f"Datos recibidos - Usuario: {usuario.user}, Contraseña: {usuario.password}")
    resultado = buscar(usuario.user, usuario.password)
    return {"validacion": f"{resultado}"}