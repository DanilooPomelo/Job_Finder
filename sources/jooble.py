import os
import httpx
import asyncio
from uni_func import loop, paggination, get_for_search
from backend.logic import save_in_db
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()



def get_jooble_jobs():
    key = os.getenv("JOOBLE_API_KEY")
    url = f"https://jooble.org/api/{key}"

    search = get_for_search()
    #encode_search = quote(search)


    payload = {
    "keywords": search,
    #"keywords": f"{search} AND (\"1 day ago\" OR \"24 hours ago\" OR \"today\")",
    "location": "",
    "page": 1,
    "ResultOnPage": 100,
    
}

    headers= {"Content-Type": "application/json",}

    response = httpx.post(url, json=payload, headers=headers)
    

    if response.status_code !=200:
       print(f"Error: {response.status_code}")
       print(response.text[:300])
    else:
        data = response.json()
        jooble_adaptor(data['jobs'])
        payload['page'] = 2
        total_count = data['totalCount']
        for page in paggination(total_count):
            payload["page"] = page
            response = httpx.post(url, json=payload, headers=headers)
            if response.status_code==200:
                    data =response.json()
                    jooble_adaptor(data['jobs'])
                    


def jooble_adaptor(jobs):
    joobler = []
    for job in jobs:
        norm_d = datetime.fromisoformat(job.get("updated", "")).date()
        
        jobles = {
                    "source": "JOOBLE",
                    "title": job['title'],
                    "company": job.get("company", ""),
                    "location":job.get("location", ""),
                    "url": job.get("link"),
                    "snippet":job.get("snippet", ""),
                    "updated": norm_d
        
                }
        joobler.append(jobles)
    asyncio.run(save_in_db(joobler), loop_factory=loop)
    for job in joobler:
        print(job['title'],"---" , job['updated'])