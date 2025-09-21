from fastapi import APIRouter,Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm   

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool
    
class UserDB(User):
    password: str

users_db = {
    "mouredev":{"username": "mouredev",
                "full_name": "brais moure",
                "email": "braismoure@mouredev.com",
                "disable": False,
                "password": "654321" 
    },
    "mouredev2":{"username": "mouredev2",
                "full_name": "brais moure2",
                "email": "braismoure@mouredev2.com",
                "disable": True,
                "password": "654321" 
    }
} 

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) 
    
async def current_user(token: str = Depends(oauth2)):
    print("llegue")
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail= "Credenciales de autenticacion invalidas (estas autenticado mas no estas autorizado)", headers={"WWW-Authenticate": "Bearer"}
        )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Usuario inactivo"
        )
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="El usuario no es correcto"
        )
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto"
        )
    print("funciona")
    return {"access_token": user.username, "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    print("me")
    return user