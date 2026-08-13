import os
import httpx
import asyncio
from uni_func import loop
from backend.logic import save_in_db
from dotenv import load_dotenv

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


def arbeitnow_adaptor(jobs):
    arbeit = []
    for job in jobs:
        arbe = {
           "source": "ARBEITNOW",
            "title": job["title"],
            "company":job["company_name"],
            "location":job["remote"],
            "url":job["url"],
            "snippet":job["description"],
            "updated":job["created_at"] 
        }
        arbeit.append(arbe)
    asyncio.run(save_in_db(arbeit), loop_factory=loop)
