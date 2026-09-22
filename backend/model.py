from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from sqlalchemy import Date , ForeignKey
from datetime import date

class Job(Base):
    __tablename__ = "Jobs"

    id: Mapped[int] =mapped_column(primary_key=True)
    title: Mapped[str]
    company: Mapped[str]
    location: Mapped[str]
    url:Mapped[str] = mapped_column(unique=True)
    snippet:Mapped[str]
    updated: Mapped[date] = mapped_column(Date, nullable=True)
    source: Mapped[str]
    first_seen: Mapped[date] = mapped_column(Date, nullable=True)
    last_seen:Mapped[date] = mapped_column(Date, nullable=True)


class CandidateProfile(Base):
    __tablename__ = "user_answer"

    id: Mapped[int] = mapped_column(primary_key=True)
    main_prof: Mapped[str]
    skills: Mapped[str]
    frameworks: Mapped[str]
    sqls:Mapped[str]
    level:Mapped[int]
    remote:Mapped[bool]


class AiJob(Base):
    __tablename__ = "job_ai_reviews"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("Jobs.id"), unique=True)
    status: Mapped[str]
    match_score: Mapped[int] = mapped_column(nullable=True)
    reason: Mapped[str]= mapped_column(nullable=True)
    missingskills: Mapped[str] = mapped_column(nullable=True)
    model: Mapped[str]= mapped_column(nullable=True)
    ai_checked_at: Mapped[date]=mapped_column(Date,nullable=True)

    job: Mapped["Job"] = relationship()