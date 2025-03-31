from sqlalchemy import Column, String, TIMESTAMP, Integer, DateTime, UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid


Base = declarative_base()


class Url(Base):
    __tablename__ = "url"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    original_url = Column(String(2048), nullable=False)
    short_code = Column(String(32), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(Integer, default=0)
    last_clicked_at = Column(DateTime, nullable=True)
