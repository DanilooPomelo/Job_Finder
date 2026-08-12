import asyncio
import sys
import httpx
from urllib.parse import quote
from dotenv import load_dotenv
import os
from backend.logic import save_in_db, get_remote
import selectors
import math


loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())
load_dotenv()
def paggination(tcount: float|int ):
    
    if tcount > 100:
        max_pages = math.ceil(tcount / 100)
        print(f"{max_pages} - страниц")
#""""""""к примеру 43.5 страниц как задать лимит так чтобы вывод был 44 страницы
        
        return range(2, max_pages +1)



def get_for_search():
    input("Search Job: ")

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
        page = 2
        job = data['results']
        title = job['title']



        #data['totalCount'][5]
        #for job in data['jobs']:
        #    print(job["title"], job['company'], job['url'])







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
        payload['page'] = 2
        total_count = data['totalCount']
        for page in paggination(total_count):
            
            payload["page"] = page
            response = httpx.post(url, json=payload, headers=headers)


            


            
            if response.status_code==200:
                    data =response.json()
                    
                                    
                    asyncio.run(
                    save_in_db(data['jobs']),
                    loop_factory=loop
            )
        

        #print(data["page"])
        print(data["totalCount"])
        #$print(data['jobs'])
        #for job in data["jobs"]:
        #    print(job["title"], "-", job["company"], )
        
    
        print(f"saved in db")


while True:
    choice = int(input("choose: "))
    if choice == 1:
        get_jooble_jobs()
    elif choice ==2:
        asyncio.run(get_remote(),loop_factory=loop)
    elif choice == 3:
        get_adzuna()