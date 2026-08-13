import asyncio
import sys
import httpx
from urllib.parse import quote
from dotenv import load_dotenv
import os
from backend.logic import save_in_db, get_remote, jooble_adaptor,adzuna_adaptor
import selectors
import math


loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())
load_dotenv()
def paggination(tcount: float|int ):
    
    if tcount > 100:
        max_pages = math.ceil(tcount / 100)
        print(f"{max_pages} - страниц")

        
        return range(2, max_pages +1)
    else: 
        return range(2,2)
        




def get_for_search():
    search = input("Search Job: ")
    return search

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
        






def get_jooble_jobs():
    key = os.getenv("JOOBLE_API_KEY")
    url = f"https://jooble.org/api/{key}"

    search = get_for_search()
    #encode_search = quote(search)


    payload = {
    "keywords": search,
    "location": "",
    "page": 1,
    "ResultOnPage": 100
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



while True:
    choice = int(input("choose: "))
    if choice == 1:
        get_jooble_jobs()
    elif choice ==2:
        asyncio.run(get_remote(),loop_factory=loop)
    elif choice == 3:
        get_adzuna()