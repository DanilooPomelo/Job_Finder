import os
import httpx
import asyncio
from uni_func import loop, get_for_search, paggination
from backend.logic import save_in_db
from dotenv import load_dotenv
from datetime import datetime
from backend.database import as_session



load_dotenv()



async def get_jobs_himalay(search):
        print("HIMALAY START")
    
    #search = get_for_search()
    #encode_search = quote(search)

        url = "https://himalayas.app/jobs/api/search"

        params = {
        "q": search,
        "sort": "recent",
        "page": 1
        
    }
        async with httpx.AsyncClient() as c:
            response =await c.get(url, params=params)
            data = response.json()
            print(data['totalCount'])
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(response.text[:300])
            else:
                data = response.json()
                await himalays_adapter(data['jobs'])
                params['page'] = 2
                t_count= data['totalCount']
                for page in paggination(t_count, 20):
                    params['page'] = page
                    response =await c.get(url, params=params)
                    if response.status_code==200:
                        data = response.json()
                        await himalays_adapter(data['jobs'])
        print("HIMALAY DONE")
    


async def himalays_adapter(jobs):
    
        hymal = []
        for job in jobs:
            norm_d = datetime.fromtimestamp(job['pubDate']).date()

            hymales = {
            "source": "HYNALAYAS",
            "title": job['title'],
            "company": job['companyName'],
            "location": job['locationRestrictions'],
            "url": job['applicationLink'],
            "snippet": job['excerpt'],
            "updated": norm_d
        }
            hymal.append(hymales)
        await save_in_db(hymal)
