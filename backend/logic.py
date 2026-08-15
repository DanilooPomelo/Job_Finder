import selectors

from sqlalchemy.dialects.postgresql import insert as pg_insert
from backend.database import as_session,engine
from backend.model import Job, CandidateProfile
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
import time
from datetime import datetime, timedelta
import asyncio




def timer_time(func):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        midle =await func(*args,**kwargs)
        end = time.perf_counter()

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




    

async def save_in_db(jobs):
    saved = 0
    duplicate = 0
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
            
            result = await s.execute(stmt)
            inserted_id = result.scalar_one_or_none()
            if inserted_id is not None:
                saved+=1
            else:
                duplicate += 1
        await s.commit()
    print(f"Новых: {saved} | Дубликатов: {duplicate}")


async def sort_by_need():
    async with as_session() as s:
        
        sorted = []
        
        positive_words = {
    "python": 4,
    "backend": 4,
    "junior": 4,
    "entry level": 4,
    "fastapi": 3,
    "rest api": 3,
    "postgresql": 2,
    "sql": 2,
    "sqlalchemy": 2,
    "django": 2,
    "middle": 2,
}

        negative_words = {
    "senior": -7,
    "lead": -7,
    "principal": -7,
    "architect": -7,
}
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        for job in jobs:
            score = 0
            text = f"{job.title}, {job.snippet}".lower()
            for word, points in positive_words.items():
                if word in text:
                    score += points
            for word, points in negative_words.items():
                if word in text:
                    score += points
            sorted.append((score, job.title, job.company, job.url,job.snippet))
        return sorted
            
                    

                    
async def get_last3():
   
    async with as_session() as s:
        now = datetime.now().date()
        treed = now - timedelta(days=3)
        last3 = []
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        for job in jobs:
            snp = job.snippet[:125]
            if job.updated >= treed:
                last3.append(f"Name: {job.title}\n\n---->>>{snp}\n\n---->{job.updated}\n\n------>>>{job.url}")
        return last3







    

async def get_new_vac():

    positive_words = {
                    "python": 4,
                    "backend": 4,
                    "junior": 4,
                    "entry level": 4,
                    "fastapi": 3,
                    "rest api": 3,
                    "postgresql": 2,
                    "sql": 2,
                    "sqlalchemy": 2,
                    "django": 2,
                    "middle": 2,
                    "remote":4
    }
    
    negative_words = {
                        "senior": -7,
                        "lead": -7,
                        "principal": -7,
                        "architect": -7,
    }
    async with as_session() as s:
        new_vac = []
        
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        now = datetime.now().date()
        for job in jobs:
            text = f"{job.title}, {job.snippet}".lower()
            score = 0
            
            if job.updated == now:
                snp =job.snippet[:125]
                for word, points in positive_words.items():
                    if word in text:
                        score += points
                for word, points in negative_words.items():
                    if word in text:
                        score += points

                #new_vac.append(f"Name: {job.title} --- Description: {snp} ===> LINK:{job.url}:::SCORE: {score}")
                new_vac.append((score, job.title, job.url, snp))
                new_vac = [job for job in new_vac if job[0]>= 4]
        resalt = []
        for score, title, url, snp in new_vac:
            resalt.append(f"Name: {title} --- Description: {snp} ===> LINK:{url} ::: SCORE: {score}")

            
            
        print(f"NEW VACANCIES:", len(new_vac))
        return resalt









    
     

#сделать все через список без подсказок все верно расстваить! после чего можно делать вызов через бота! 
@timer_time
async def get_remote():
    async with as_session() as s:
        remote_j = []
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        for job in jobs:
            if job.location == "Remote":
                if job.snippet is None:
                    job.snippet = ""
                
                snippet = job.snippet[:125]
                remote_j.append(f"Name: {job.title} --- Description: {snippet} ===> LINK:{job.url}")
        

            

        return (remote_j)

