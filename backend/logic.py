import selectors

from sqlalchemy.dialects.postgresql import insert as pg_insert
from backend.database import as_session,engine
from backend.model import Job, CandidateProfile
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
import time
from datetime import datetime
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




    

async def get_new_vac():
    async with as_session() as s:
        new_vac = []
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        now = datetime.now().date()
        for job in jobs:
            print(
                job.id,
                job.first_seen,
                type(job.first_seen),
                job.first_seen == now
            )
            if job.first_seen == now:
                snp =job.snippet[:125]

                new_vac.append(f"Name: {job.title} --- Description: {snp} ===> LINK:{job.url}")
        print("NEW VACANCIES:", len(new_vac))
        return new_vac

async def get_today_vac():
    async with as_session() as s:
        new_vac = []
        q = select(Job)
        jobs = (await s.scalars(q)).all()
        now = datetime.now().date()
        for job in jobs:
            print(
                job.id,
                job.first_seen,
                type(job.first_seen),
                job.first_seen == now
            )
            if job.updated == now:
                snp =job.snippet[:125]
                
                new_vac.append(f"Name: {job.title} --- Description: {snp} ===> LINK:{job.url}")
        print("NEW VACANCIES:", len(new_vac))
        return new_vac
            



    
     

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

