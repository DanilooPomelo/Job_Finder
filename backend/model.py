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


class CandidateProfile(Base):
    __tablename__ = "user_answer"

    id: Mapped[int] = mapped_column(primary_key=True)
    main_prof: Mapped[str]
    skills: Mapped[str]
    frameworks: Mapped[str]
    sqls:Mapped[str]
    level:Mapped[int]
    remote:Mapped[bool]
