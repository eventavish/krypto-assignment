import uuid

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from db.base_class import Base


class Alert(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    user_email = Column(String, ForeignKey("user.email", ondelete="CASCADE"), index=True, nullable=False)
