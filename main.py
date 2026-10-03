import asyncio
from backend.logic import   get_new_vac, get_filtred_forai
from sources.adzuna import  get_adzuna
from sources.arbeitnow import get_arbeitnow
from sources.jooble import get_jooble_jobs
from uni_func import loop,get_for_search
from sources.hinalayas import get_jobs_himalay
from sources.remotejobs import get_jobs_remotejobs
from backend.bot.bot import main
from scheduler import autostart
from backend.ai_workers.vacancy_checker import data_for_check


async def start_app():
    await asyncio.gather(
        autostart(),
        main(),
        

    )

        

if __name__ == "__main__":
    asyncio.run(start_app(),loop_factory=loop)