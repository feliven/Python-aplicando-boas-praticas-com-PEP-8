from typing import Dict
from fastapi import FastAPI
from app.routers import routers_usuario, routers_produto

MENSAGEM_HOME: str = "Bem-vindo à API de Recomendação de Produtos"

# Criando o App
app = FastAPI()
app.include_router(routers_usuario.router)
app.include_router(routers_produto.router)


# Iniciando o servidor
@app.get("/")
def home() -> Dict[str, str]:
    return {"mensagem": MENSAGEM_HOME}
