import os
import httpx
import asyncio
from uni_func import loop, paggination, get_for_search
from backend.logic import save_in_db
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()



def adzuna_adaptor(jobs):
    adzuna = []
    for job in jobs:
        company = job.get('company') or {}
        norm_d = datetime.fromisoformat(job['created']).date()
        adzunaj = {
            "source": "ADZUNA",
            "title": job["title"],
            "company":company.get("display_name") or {},
            "location":job["location"]["display_name"],
            "url":job["redirect_url"],
            "snippet":job["description"],
            "updated":norm_d
        }
        adzuna.append(adzunaj)
    asyncio.run(save_in_db(adzuna), loop_factory=loop)



def get_adzuna():
    search = get_for_search()
    page = 1
    key = os.getenv("ADZUNA_API_KEY")
    app_id = os.getenv("ADZUNA_ID")
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"

    params = {
    "app_id": app_id,
    "app_key": key,
    "results_per_page": 100,
    "what": f"{search}",
}

    headers = {
    "Accept": "application/json"
    }

    response = httpx.get(
        url,
        params=params,
        headers=headers
    )
    if response.status_code !=200:
        print(f"Error: {response.status_code}")
        print(response.text[:300])
    else:
        data = response.json()
        job = data['results']
        adzuna_adaptor(job)
        t_count = data['count']
        
        page = 2
        for pages in paggination(t_count):
            page =pages
            url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"
            response = httpx.get(url, params=params, headers=headers)
            if response.status_code==200:
                data = response.json()
                job = data['results']
                adzuna_adaptor(job)