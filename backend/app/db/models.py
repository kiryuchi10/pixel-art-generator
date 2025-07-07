from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any

from .database import db  # From Flask SQLAlchemy instance
Base = db.Model

# ----------------------------
# User Model
# ----------------------------

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    generations = relationship("Generation", back_populates="user", cascade="all, delete")
    style_presets = relationship("StylePreset", back_populates="user", cascade="all, delete")
    color_palettes = relationship("ColorPalette", back_populates="user", cascade="all, delete")
    api_usages = relationship("ApiUsage", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

# ----------------------------
# Generation Model
# ----------------------------

class Generation(Base):
    __tablename__ = "generations"

    id = Column(String(36), primary_key=True, index=True)  # UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    input_text = Column(Text, nullable=True)
    input_image_url = Column(String(255), nullable=True)

    style_type = Column(String(50), nullable=False, default="8bit")
    resolution = Column(String(20), nullable=False, default="32x32")
    color_palette = Column(String(50), nullable=False, default="classic")
    batch_count = Column(Integer, nullable=False, default=1)
    generation_config = Column(JSON, nullable=True)

    output_image_url = Column(String(255), nullable=True)
    output_images = Column(JSON, nullable=True)

    status = Column(String(20), nullable=False, default="pending")  # pending, processing, completed, failed
    progress = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)

    processing_time = Column(Float, nullable=True)
    model_version = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="generations")
    steps = relationship("GenerationStep", back_populates="generation", cascade="all, delete")

    def __repr__(self):
        return f"<Generation(id='{self.id}', status='{self.status}')>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "input_text": self.input_text,
            "input_image_url": self.input_image_url,
            "style_type": self.style_type,
            "resolution": self.resolution,
            "color_palette": self.color_palette,
            "batch_count": self.batch_count,
            "output_image_url": self.output_image_url,
            "output_images": self.output_images,
            "status": self.status,
            "progress": self.progress,
            "error_message": self.error_message,
            "processing_time": self.processing_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

# ----------------------------
# StylePreset Model
# ----------------------------

class StylePreset(Base):
    __tablename__ = "style_presets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    config = Column(JSON, nullable=False)

    is_public = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="style_presets")

    def __repr__(self):
        return f"<StylePreset(id={self.id}, name='{self.name}')>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "config": self.config,
            "is_public": self.is_public,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# ----------------------------
# GenerationStep Model
# ----------------------------

class GenerationStep(Base):
    __tablename__ = "generation_steps"

    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(String(36), ForeignKey("generations.id"), nullable=False)

    step_number = Column(Integer, nullable=False)
    step_name = Column(String(100), nullable=False)
    step_description = Column(Text, nullable=True)

    step_image_url = Column(String(255), nullable=True)
    step_data = Column(JSON, nullable=True)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    processing_time = Column(Float, nullable=True)

    generation = relationship("Generation", back_populates="steps")

    def __repr__(self):
        return f"<GenerationStep(id={self.id}, step='{self.step_name}')>"

# ----------------------------
# ColorPalette Model
# ----------------------------

class ColorPalette(Base):
    __tablename__ = "color_palettes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    colors = Column(JSON, nullable=False)  # Array of hex color codes
    color_count = Column(Integer, nullable=False)

    is_public = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="color_palettes")

    def __repr__(self):
        return f"<ColorPalette(id={self.id}, name='{self.name}')>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "description": self.description,
            "colors": self.colors,
            "color_count": self.color_count,
            "is_public": self.is_public,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# ----------------------------
# ApiUsage Model
# ----------------------------

class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    ip_address = Column(String(100), nullable=True)
    user_agent = Column(String(255), nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="api_usages")

    def __repr__(self):
        return f"<ApiUsage(id={self.id}, endpoint='{self.endpoint}')>"
