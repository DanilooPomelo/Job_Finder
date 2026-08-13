from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base

class Job(Base):
    __tablename__ = "Jobs"

    id: Mapped[int] =mapped_column(primary_key=True)
    title: Mapped[str]
    company: Mapped[str]
    location: Mapped[str]
    url:Mapped[str] = mapped_column(unique=True)
    snippet:Mapped[str]
    updated: Mapped[str]
    source: Mapped[str]