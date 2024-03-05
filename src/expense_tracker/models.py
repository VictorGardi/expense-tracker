from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    tags: Mapped[str] = mapped_column(String(30))


engine = create_engine("sqlite:///sqlite.db", echo=True)
Base.metadata.create_all(engine)
