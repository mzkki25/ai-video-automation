from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.Database import Base

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    nama_produk = Column(String, nullable=False)
    target_audiens = Column(String, nullable=False)
    usp = Column(Text, nullable=False)
    cta = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
