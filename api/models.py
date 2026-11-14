from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from api.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    properties = relationship("Property", back_populates="owner", cascade="all, delete-orphan")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    property_id_slug = Column(String, unique=True, index=True, nullable=False)
    nome_propriedade = Column(String, nullable=False)
    municipio = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    tamanho_hectares = Column(Float, nullable=False)
    tipo_solo = Column(String, nullable=True)
    priorities = Column(JSON, default=list)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="properties")
    
    histories = relationship("CropHistory", back_populates="property", cascade="all, delete-orphan")

class CropHistory(Base):
    __tablename__ = "crop_histories"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    ano_safra = Column(String, nullable=False)
    cultura_verao = Column(String, nullable=False)
    cultura_safrinha = Column(String, nullable=True)
    produtividade_estimada_sc_ha = Column(Float, nullable=True)
    
    property = relationship("Property", back_populates="histories")