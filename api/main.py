from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
from typing import Optional

from api.database import init_db, get_db
from api.models import User, Property, CropHistory
from api.schemas import UserCreate, UserResponse, Token, PropriedadeCreate, AnaliseRequest
from rotacao.motor_biologico import MotorRotacaoBiologica

load_dotenv()

app = FastAPI(
    title="TerraTurn API - Motor de Rotação Agronômica",
    version="1.0.0"
)

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-segredo")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
motor_bio = MotorRotacaoBiologica()

@app.on_event("startup")
def startup_event():
    init_db()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    new_user = User(
        nome=user_data.nome,
        email=user_data.email,
        hashed_password=user_data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/properties", status_code=status.HTTP_201_CREATED)
def cadastrar_propriedade(prop: PropriedadeCreate, db: Session = Depends(get_db)):
    nova_prop = Property(
        property_id_slug=prop.property_id_slug,
        nome_propriedade=prop.nome_propriedade,
        municipio=prop.municipio,
        latitude=prop.latitude,
        longitude=prop.longitude,
        tamanho_hectares=prop.tamanho_hectares,
        tipo_solo=prop.tipo_solo,
        priorities=prop.priorities,
        user_id=1
    )
    db.add(nova_prop)
    db.commit()
    db.refresh(nova_prop)
    return {"mensagem": "Propriedade cadastrada com sucesso!", "id": nova_prop.id}