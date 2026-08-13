import asyncio
from backend.logic import  get_remote
from sources.adzuna import  get_adzuna
from sources.arbeitnow import get_arbeitnow
from sources.jooble import get_jooble_jobs
from uni_func import loop






        


if __name__ == "__main__":
    while True:
        choice = int(input("choose: "))
        if choice == 1:
           get_jooble_jobs()
        elif choice ==2:
             asyncio.run(get_remote(),loop_factory=loop)
        elif choice == 3:
            get_adzuna()
        elif choice ==4:
            get_arbeitnow()