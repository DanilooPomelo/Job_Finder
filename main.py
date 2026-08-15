import asyncio
from backend.logic import  get_remote, get_new_vac, sort_by_need
from sources.adzuna import  get_adzuna
from sources.arbeitnow import get_arbeitnow
from sources.jooble import get_jooble_jobs
from uni_func import loop,get_for_search
from sources.hinalayas import get_jobs_himalay
from sources.remotejobs import get_jobs_remotejobs




        

if __name__ == "__main__":
    while True:
        choice = int(input("choose: "))
        if choice == 1:
           #get_jooble_jobs("Junior Python Developer")
#        elif choice ==2:
#             asyncio.run(get_remote(),loop_factory=loop)
#        elif choice == 3:
#            get_adzuna()
#        elif choice ==4:
#            get_arbeitnow()
#        elif choice == 5:
#            asyncio.run(get_new_vac(),loop_factory=loop)
#        elif choice == 6:
#            get_jobs_himalay()
#        elif choice == 7:
#            get_jobs_remotejobs()