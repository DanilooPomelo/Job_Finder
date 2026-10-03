from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from sqlalchemy import Date , ForeignKey, BigInteger,Text
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
    telegram_id = mapped_column(BigInteger, nullable=True, index=True)
    name:Mapped[str]
    phone:Mapped[str]
    email:Mapped[str]
    location:Mapped[str]
    summary:Mapped[str]= mapped_column(Text)
    expirience:Mapped[str]= mapped_column(Text)
    education:Mapped[str]= mapped_column(Text)


    main_prof: Mapped[str]
    skills: Mapped[str]= mapped_column(Text)
    frameworks: Mapped[str]
    sqls:Mapped[str]
    langs:Mapped[str]= mapped_column(Text)
    projects:Mapped[str]= mapped_column(Text)
    github:Mapped[str]
    ln:Mapped[str]
    created_at:Mapped[date] = mapped_column(Date, nullable=True)
    upd_at:Mapped[date] = mapped_column(Date, nullable=True)
    


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



class GenCV(Base):
    __tablename__ = "vac_cv"
    id: Mapped[int] = mapped_column(primary_key=True)
    vac_rew_id:Mapped[int] = mapped_column(ForeignKey("job_ai_reviews.id"))
    job_id:Mapped[int] =mapped_column(ForeignKey("Jobs.id"))
    user_id:Mapped[int] = mapped_column(ForeignKey("user_answer.id"))
    title: Mapped[str]
    summary: Mapped[str]= mapped_column(Text)
    experience: Mapped[str]= mapped_column(Text)
    education: Mapped[str]= mapped_column(Text)
    skills: Mapped[str]= mapped_column(Text)
    frameworks: Mapped[str]
    sqls: Mapped[str]
    languages: Mapped[str]= mapped_column(Text)
    projects: Mapped[str]= mapped_column(Text)

    created_at: Mapped[date] = mapped_column(Date)


    job:Mapped["Job"]= relationship()
    aijob:Mapped["AiJob"]= relationship()
    cprofile:Mapped["CandidateProfile"]= relationship()
    