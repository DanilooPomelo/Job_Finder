import selectors

from sqlalchemy.dialects.postgresql import insert as pg_insert
from backend.database import as_session,engine
from backend.model import Job, CandidateProfile, AiJob
from sqlalchemy import select, or_
from sqlalchemy.orm import Session, selectinload
import time
from datetime import datetime, timedelta
import asyncio




def timer_time(func):
    async def wrapper(*args, **kwargs):
        print("START")
        start = time.perf_counter()
        midle =await func(*args,**kwargs)
        end = time.perf_counter()
        print("WND")

        print(f"function result in {end - start:.4f} seconds")
        return midle
    return wrapper

async def save_user_cv(a: dict):
    async with as_session() as s:
        
            stmt = pg_insert(CandidateProfile).values(
                        main_prof=a['user_prof'] ,
                        skills=a['user_skills'],
                        frameworks=a['user_frameworks'],
                        sqls=a['user_sqls'],
                        level=a['user_level'],
                        remote=False
                    )
            await s.execute(stmt)
            await s.commit()
async def get_pg(result, page):
    start = (page - 1) * 5
    end = page * 5

    return result[start:end]
async def save_in_ai_table(tname):
    async with as_session() as s:
        for score, jid in tname:
            stmt = pg_insert(AiJob).values(
                job_id=jid,
                status="new",
                match_score=score
            )
            await s.execute(stmt)
        await s.commit()         
async def save_in_db(jobs):
    
    async with as_session() as s:
        for job in jobs:
            now = datetime.now().date()
            
            stmt = pg_insert(Job).values(
                title=job["title"],
                company=job["company"],
                location=job["location"],
                url=job["url"],
                snippet=job["snippet"],
                updated=job["updated"],
                source=job['source'],
                first_seen=now,
                last_seen=now
            ).on_conflict_do_update(index_elements=["url"],set_={"last_seen":now})
            
            await s.execute(stmt)
            
        await s.commit()



    

                       
async def get_last3():
   
    async with as_session() as s:
        now = datetime.now().date()
        treed = now - timedelta(days=3)
        last3 = []
        q = select(Job).where(Job.updated >= treed)
        jobs = (await s.scalars(q)).all()
        for job in jobs:
            snp = job.snippet[:125]
            
            last3.append(f"Name: {job.title}\n\n---->>>{snp}\n\n---->{job.updated}\n\n------>>>{job.url}")
        return last3



async def scoring(jobs):
    results = []

    for job in jobs:
        score = 0

        text = f"{job.title} {job.snippet}".lower()

        for dict_rule in SCORING_RULES.values():
            for word, points in dict_rule.items():
                if word in text:
                    score += points

        results.append(
            (
                score,
                job.title,
                job.url,
                job.snippet[:250],
                job.id
            )
        )

    return results

async def get_filtred_forai():
    async with as_session() as s:
        filtred = []
        now = datetime.now().date()
        q = select(Job).where(Job.updated == now)
        
        jobs = (await s.scalars(q)).all()
        res = await scoring(jobs)
        for score,title,url,snippet, jid in res:
            q = select(AiJob).where(AiJob.job_id == jid)
            exists = await s.scalar(q)
            if exists:
                continue
            if score > 5:
                filtred.append((score,jid))
        await save_in_ai_table(filtred)

async def get_new_vac():
    async with as_session() as s:
        new_vac = []
        now = datetime.now().date()
        q = select(Job).where(Job.updated == now)
        jobs = (await s.scalars(q)).all()
        
        results = await scoring(jobs)
        
        for score,title, url,snp,jid in results:
            if score > 5:
                new_vac.append((score, title, url, snp[:250]))
            
           

        
        resalt = []
        for score, title, url, snp in new_vac:
            resalt.append(f"Name: {title} --- \n\n Description: {snp[:250]} ===> \n\nLINK:{url} :::\n\n SCORE: {score}")

            
            
        print(f"NEW VACANCIES:", {len(new_vac)})
        return resalt


async def get_accepted_vac():
    async with as_session() as s:
        ac_vac = []
        q = select(AiJob).options(selectinload(AiJob.job)).where(AiJob.status == "accepted")
        a_j = (await s.scalars(q)).all()
        for j in a_j:
            
            ac_vac.append(f"Name: {j.job.title}\n\nStatus: {j.status}\n\nScores: {j.match_score}\n\n Reason: {j.reason}\n\nMissing Skills: {j.missingskills}\n\nJob URL: {j.job.url}")
        return ac_vac



    
    

# ============================================================
# TITLE SCORING
# ============================================================

STRONG_POSITIVE = {
    # Python
    "python": 5,
    "python developer": 6,
    "python backend": 6,
    "backend python": 6,

    # Backend frameworks
    "fastapi": 5,
    "django": 4,
    "flask": 3,

    # API
    "rest api": 4,
    "restful api": 4,
    "api development": 4,
    "web api": 3,

    # Database
    "sql": 3,
    "postgresql": 4,
    "postgres": 4,
    "sqlite": 2,
    "sqlalchemy": 4,
    "orm": 2,

    # Async
    "asyncio": 4,
    "async python": 4,
    "asynchronous": 2,
    "async": 2,

    # Development
    "git": 2,
    "github": 2,

    # Testing
    "pytest": 3,
    "unit testing": 2,
    "unit tests": 2,

    # Docker / Linux
    "docker": 2,
    "docker compose": 2,
    "linux": 2,
}


POSITIVE = {
    # Python ecosystem
    "pydantic": 2,
    "poetry": 1,
    "pip": 1,
    "virtualenv": 1,

    # Backend
    "http": 1,
    "httpx": 2,
    "json": 1,
    "web services": 2,
    "microservices": 2,

    # Databases
    "mysql": 1,
    "mariadb": 1,
    "redis": 2,
    "database": 1,
    "relational database": 2,
    "database design": 2,
    "database migration": 2,
    "migrations": 1,

    # Async / background
    "celery": 2,
    "rabbitmq": 1,
    "kafka": 1,
    "message queue": 1,
    "background jobs": 1,

    # Auth
    "jwt": 2,
    "oauth": 1,
    "authentication": 1,
    "authorization": 1,

    # DevOps
    "ci/cd": 2,
    "cicd": 2,
    "github actions": 2,
    "gitlab ci": 2,
    "nginx": 1,
    "bash": 1,

    # Cloud
    "aws": 1,
    "azure": 1,
    "gcp": 1,
    "cloud": 1,

    # Architecture
    "clean architecture": 1,
    "design patterns": 1,
    "solid": 1,
    "oop": 2,

    # Frontend — secondary
    "javascript": 1,
    "react": 1,
    "typescript": 1,

    # Other backend
    "web scraping": 2,
    "scraping": 2,
    "parser": 1,
    "parsing": 1,
}


NEGATIVE = {
    # Seniority
    "senior": -5,
    "senior developer": -6,
    "senior python developer": -6,

    "lead": -7,
    "team lead": -7,
    "tech lead": -7,

    "principal": -8,
    "principal engineer": -8,
    "staff engineer": -8,

    "architect": -8,
    "software architect": -8,
    "solutions architect": -8,

    "engineering manager": -8,
    "engineering director": -8,

    # Too much experience
    "5+ years": -4,
    "6+ years": -5,
    "7+ years": -6,
    "8+ years": -7,
    "10+ years": -8,

    # Other main languages
    "java developer": -5,
    "c# developer": -5,
    ".net developer": -5,
    "c++ developer": -5,
    "golang developer": -5,
    "go developer": -5,
    "ruby developer": -5,
    "php developer": -5,
}

LEVEL_SCORE = {
    "intern": 2,
    "internship": 2,
    "trainee": 2,

    "entry level": 3,
    "entry-level": 3,

    "junior": 4,
    "junior developer": 4,
    "junior python": 5,
    "junior python developer": 6,

    "middle": 1,
    "mid": 1,
    "mid-level": 1,
    "middle developer": 1,
    "middle python": 2,
    "middle python developer": 2,

    "senior": -5,
    "senior developer": -6,
}
LOCATION_SCORE = {
    "moldova": 4,
    "chisinau": 4,
    "europe": 2,
    "eu": 2,
}
SCORING_RULES = {
    "strong": STRONG_POSITIVE,
    "positive": POSITIVE,
    "negative": NEGATIVE,
}