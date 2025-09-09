from sqlalchemy import String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column
from db import Base

class Animal(Base):
    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    habitat: Mapped[str] = mapped_column(Text)
    food: Mapped[str] = mapped_column(String(200))
    behaviour: Mapped[str] = mapped_column(Text)
    unique: Mapped[str] = mapped_column(Text)
    addition: Mapped[str] = mapped_column(Text)