from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model import User, UserInDB, UserNew
from database import collection_users
from typing import Annotated, Union
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

SECRET_KEY = "823436f933842b8f37bec808e160ea7d0d990138df12081eb165280490de22cc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    },
    "alice": {
        "username": "johndoe",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2"
    },
}

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db, username: str):
    user_dict = await db.find_one({"username": username})
    del user_dict["_id"]
    return UserInDB(**user_dict)

async def authenticate_user(collection_users, username: str, password: str):
    user = await get_user(collection_users, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print("lol", username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user_in_db = await get_user(collection_users, username=token_data.username)
    if user_in_db is None:
        raise credentials_exception
    return User(**user_in_db.dict(exclude={"hashed_password"}))


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    print("This is my form data",form_data.username, form_data.password)
    user = await authenticate_user(collection_users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


#get current user
@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

#register as new user
@router.post("/register")
async def insert_user(user: UserNew):
    try:
        # Convert the User instance to a dictionary
        user_dict = user.dict()
        # hash password
        hashedPassword = get_password_hash(user_dict["password"])
        # save user in the database
        del user_dict["password"]
        user_dict["hashed_password"] = hashedPassword
        
        result = await collection_users.insert_one(user_dict)
        user_in_db = await collection_users.find_one({"_id": result.inserted_id})
        user_in_db["id"] = str(user_in_db["_id"])
        del user_in_db["_id"]
        del user_in_db["hashed_password"]
        print(user_in_db)
        return user_in_db
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

        

# verify if token is valid
@router.get("/verify")
async def verify_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user









#Annotated is used to attach metadata to type hints, here it combiens type hint with dependency injection
#Here, Annotated is a way to say "this is a str that is obtained via Depends(oauth2_scheme)."


