from fastapi import FastAPI
from routers import products,jwt_auth_users,users,basic_auth_users,users_db

app = FastAPI()

#routeers
app.include_router(products.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users.router)
app.include_router(users_db.router)


 
@app.get('/perfil/{nombre}')
async def saludo(nombre: str):
  return {f'hola{nombre}'}