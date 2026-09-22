import os
import httpx
import asyncio
from uni_func import loop, get_for_search, paggination
from backend.logic import save_in_db
from dotenv import load_dotenv
from datetime import datetime
from backend.database import as_session

async def get_jobs_remotejobs(search):
    try:
        
    #search = get_for_search()


        url = "https://remotejobs.org/api/v1/jobs"

        params = {
        "q": search,
        "limit": 50,
        "page": 1
    }
        async with httpx.AsyncClient() as c:
            response =await c.get(url, params=params)
            if response.status_code !=200:
                print(f"Error: {response.status_code}")
                print(response.text[:300])
                er = response.status_code
                return er
            else:
                data = response.json()
                await adapt_remote(data['data'])
                params['page'] = 2
                t_count = data['pagination']['total']
                for page in paggination(t_count, 50):
                    params["page"] = page
                    response =await c.get(url, params=params)
                    if response.status_code == 200:
                        data =response.json()
                        await adapt_remote(data['data'])
    except Exception as e:
        print(f"REMOTEJOBS ERROR {e}")
                       


async def adapt_remote(jobs):
    
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
        await save_in_db(remotes)

    
    