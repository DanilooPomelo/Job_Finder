import os
import httpx
import asyncio
from uni_func import loop
from backend.logic import save_in_db
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()




def get_arbeitnow():
    url = "https://www.arbeitnow.com/api/job-board-api"

    response = httpx.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text[:300])
    else:
        data = response.json()
        job = data['data']
        arbeitnow_adaptor(job)

def arbeit_norm_time(jobs):
    for job in jobs:
        pass
         

def arbeitnow_adaptor(jobs):
    arbeit = []
    for job in jobs:
        norm_data = datetime.fromtimestamp(job['created_at']).date()
        
        arbe = {
           "source": "ARBEITNOW",
            "title": job["title"],
            "company":job["company_name"],
            "location":job["remote"],
            "url":job["url"],
            "snippet":job["description"],
            "updated":norm_data
        }
        arbeit.append(arbe)
    asyncio.run(save_in_db(arbeit), loop_factory=loop)
