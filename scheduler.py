#from apscheduler import AsyncScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from apscheduler.triggers.cron import CronTrigger
from sources.adzuna import  get_adzuna
from sources.arbeitnow import get_arbeitnow
from sources.jooble import get_jooble_jobs
from uni_func import loop,get_for_search, timeouts_src, retry_func
from sources.hinalayas import get_jobs_himalay
from sources.remotejobs import get_jobs_remotejobs
from sqlalchemy import text
from backend.database import as_session
from backend.logic import get_filtred_forai
from backend.ai_workers.vacancy_checker import data_for_check


async def start():
#only for my self use becuase DB Neon is Free and needed for out sleep
    async with as_session() as s:
        try:
            await s.execute(text("SELECT 1"))
        except Exception as e:
            print(f"waky waky NEON {e}")
    await asyncio.sleep(30)
########################################################################


    searcher = ["Junior Python Developer",
    "Junior Python Backend Developer",
    "Junior Backend Developer Python",
    "Junior Backend Engineer Python",
    "Junior Python Software Engineer",
    "Entry Level Python Developer",
    "Entry Level Backend Developer",
    "Python Developer",
    "Python Backend Developer",
    "Python API Developer",
    "Python Software Engineer",
    "Backend Developer Python",
    "Python FastAPI Developer",
    "Python Django Developer",
    "Junior Software Engineer Python",]
    for s in searcher:
        await asyncio.gather(
            timeouts_src(get_jobs_remotejobs,s),
            timeouts_src(get_jobs_himalay,s),
            timeouts_src(get_adzuna,s),
            timeouts_src(get_arbeitnow),
            timeouts_src(get_jooble_jobs,s)
            )

        await asyncio.sleep(15)

    retry_func(await get_filtred_forai)

    retry_func(await data_for_check)
        


async def autostart():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        start,
        CronTrigger(
            hour="8,20,14",
            minute=00,
            timezone="Europe/Chisinau"
        )
    )
    scheduler.start()

    await asyncio.Event().wait()
    
    


