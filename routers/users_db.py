from fastapi import APIRouter,HTTPException,status
from db.models.user import User
from db.schemas.user import user_schema,users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=['userdb'],
                   responses={status.HTTP_404_NOT_FOUND : {"message":"No encontrado"}})

#entidad users



@router.get('/', response_model=list[User])
async def users():
    return users_schema(db_client.users.find())
    
        
    

#path
@router.get('/{id}')
async def user(id: str):
    return search_user("_id",ObjectId(id))
#query  
@router.get('/query')
async def user(id: str):
    return search_user("_id",ObjectId(id))
        

@router.post('/',response_model=User,status_code=status.HTTP_201_CREATED)
async def user(user:User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status_code=409,detail= "El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]
     
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id":id}))
    
    return User(**new_user)


@router.put('/',status_code=202)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)},user_dict)
    except:
        return {"Error":"No se ha actualizado el usuario"}
    return search_user("_id",ObjectId(user.id))
            

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)}) 
    
    if not found:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"error":"no se ha encontrado el usuario a eliminar"})
    
    
 
    
def search_user(field: str, key):
    try:
        user = user_schema(db_client.users.find_one({field:key}))
        return User(**user)
    except:
        return {"Error": "No se ha encontrado el usuario"}




def validar_usuarios_repetidos(user: int):
    users = filter(lambda x: x == user, users_list)
    try:
        return list(users)[0]
    except:
        return {'error':'no se ha podido encontrar este usuario'}
