#from apscheduler import AsyncScheduler


from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from apscheduler.triggers.cron import CronTrigger
from sources.adzuna import  get_adzuna
from sources.arbeitnow import get_arbeitnow
from sources.jooble import get_jooble_jobs
from uni_func import loop,get_for_search
from sources.hinalayas import get_jobs_himalay
from sources.remotejobs import get_jobs_remotejobs

async def start():
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
        await asyncio.gather(get_jobs_remotejobs(s),
        get_jobs_himalay(s),
        get_adzuna(s),
        get_arbeitnow(),
        get_jooble_jobs(s))

        await asyncio.sleep(120)
        


async def autostart():
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        start,
        CronTrigger(
            hour="8,20,18,19",
            minute=46,
            timezone="Europe/Chisinau"
        )
    )
    scheduler.start()

    await (asyncio.sleep(99999999999))
    
    
asyncio.run(autostart(), loop_factory=loop)

