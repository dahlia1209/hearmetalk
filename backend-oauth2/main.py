from fastapi import FastAPI, Depends, HTTPException, status,Query
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import httpx
import os
from sqlalchemy.orm import Session
from typing import Optional
from dotenv import load_dotenv

# import crud, models, schemas
# from database import SessionLocal, engine
# models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://www.hearmetalk.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2設定
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    tokenUrl="https://oauth2.googleapis.com/token",
    refreshUrl="https://oauth2.googleapis.com/token",
    scheme_name="Google"
)

# ここにあなたのクライアント情報を設定してください
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = os.getenv("SCOPES")

@app.get("/auth")
async def auth(redirect_url:Optional[str]=None):
    local_redirect_url = os.getenv("REDIRECT_URI") if redirect_url==None else redirect_url
    if redirect_url==None:
        return  
    return RedirectResponse(url=f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={local_redirect_url}&scope={SCOPES}&access_type=offline&state=state_value&include_granted_scopes=true")

@app.get("/auth/callback")
async def auth_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
    response.raise_for_status()
    tokens = response.json()
    return tokens
    # pre_auth_redirect_url = "http://localhost:5173"
    # return RedirectResponse(pre_auth_redirect_url)


@app.post("/refresh_token")
async def refresh_token(refresh_token: str):
    url = "https://oauth2.googleapis.com/token"
    data = {
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to refresh token")
        return response.json()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
