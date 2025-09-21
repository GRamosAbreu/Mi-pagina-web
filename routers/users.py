from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter()

#entidad users

class User(BaseModel):
    id: int 
    name: str
    surname: str
    url:str
    age:int
    
users_list = [User(id=1,name='brais',surname='moure',url='itch.io/galecox',age=35),
         User(id=2,name='andres',surname='montenegro',url='itch.io/galecox',age=23),
         User(id=3,name='angelica',surname='ramos',url='itch.io/galecox',age=25),
         User(id=4,name='lucia',surname='ramirz',url='itch.io/galecox',age=  35)
        ]
# @app.get('/perfil/{nombre}')
# async def userjasons(nombre: str):
#     return [{'nombre':nombre,'apellido':'ramos','url':'itch.io/galecox'},
#             {'nombre':'andres','apellido':'ramos','url':'itch.io/andres'},
#             {'nombre':'alejandro','apellido':'ramos','url':'itch.io/alejandro'},
#             {'nombre':'sofia','apellido':'ramos','url':'itch.io/sofia'}
#             ]
@router.get('/users')
async def users():
    return users_list


#path
@router.get('/user/{id}')
async def user(id: int):
    user =  search_users(id)
    if user is None:    
        raise HTTPException(status_code=404,detail= "No se ha encontrado el usuario")
    return user
#query  
@router.get('/userquery')
async def user(id: int):
    user =  search_users(id)
    if user is None:
        raise HTTPException(status_code=404,detail= "No se ha encontrado el usuario")
    return user
        

@router.post('/user',status_code=201)
async def user(user:User):
    if type(search_users(user.id)) == User:
        raise HTTPException(status_code=409,detail= "El usuario ya existe")

    users_list.append(user)
    return user
    
@router.put('/user',status_code=202)
async def user(user: User):
    found = False
    for index,saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        raise HTTPException(status_code=404,detail="No se ha encontrado el usuario a cambiar")
    else:
        return user
            

@router.delete('/user/{id}')
async def delete_user(id: int):
    found = False
    for index,saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"mensaje":"se ha deleteado el usuario correctamente"}
    if not found:
        raise HTTPException(status_code=404,detail="No se ha encontrado el usuario a borrar")
            
    
    
 
    
def search_users(id: int):
    resultado = next((user for user in users_list if user.id == id), None)
    if resultado:
        return resultado





def validar_usuarios_repetidos(user: int):
    users = filter(lambda x: x == user, users_list)
    try:
        return list(users)[0]
    except:
        return {'error':'no se ha podido encontrar este usuario'}
