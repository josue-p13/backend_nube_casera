from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rutas_usuario import router as usuario_router
from rutas_archivos import router as archivos_router
from rutas_gestion import router as gestion_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(archivos_router)
app.include_router(gestion_router)