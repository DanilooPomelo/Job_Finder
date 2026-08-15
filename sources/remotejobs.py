import os
import httpx
import asyncio
from uni_func import loop, get_for_search, paggination
from backend.logic import save_in_db
from dotenv import load_dotenv
from datetime import datetime

def get_jobs_remotejobs():
    search = get_for_search()


    url = "https://remotejobs.org/api/v1/jobs"

    params = {
        "q": search,
        "limit": 50,
        "page": 1
    }

    response = httpx.get(url, params=params)
    if response.status_code !=200:
        print(f"Error: {response.status_code}")
        print(response.text[:300])
    else:
        data = response.json()
        adapt_remote(data['data'])
        params['page'] = 2
        t_count = data['pagination']['total']
        for page in paggination(t_count, 50):
            params["page"] = page
            response = httpx.get(url, params=params)
            if response.status_code == 200:
                data =response.json()
                adapt_remote(data['data'])


def adapt_remote(jobs):
    remotes = []
    for job in jobs:
        norm_d = datetime.fromisoformat(job['posted_at']).date()
        remote = {
            "source": "REMJOBS",
            "title": job['title'],
            "company": job['company']['name'],
            "location":job['location'],
            "url": job['url'],
            "snippet":job['description'],
            "updated": norm_d
                    
        }
        remotes.append(remote)
    asyncio.run(save_in_db(remotes), loop_factory=loop)

    
    