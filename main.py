import asyncio
import sys
import httpx
from urllib.parse import quote
from dotenv import load_dotenv
import os
from backend.logic import save_in_db, get_remote
import selectors


loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())
load_dotenv()


        



def get_jobs():
    key = os.getenv("JOOBLE_API_KEY")
    url = f"https://jooble.org/api/{key}"

    search = input("Search Job:  ")
    encode_search = quote(search)


    payload = {
    "keywords": search,
    "location": ""
}

    headers= {
   
    "Content-Type": "application/json",
    
}

    response = httpx.post(url, json=payload, headers=headers)
    if response.status_code !=200:
       print(f"Error: {response.status_code}")
       print(response.text[:300])
    else:
        data = response.json()
        print(data["totalCount"])
        for job in data["jobs"]:
            print(job["title"], "-", job["company"])
        
    if response.status_code==200:
        data =response.json()
        asyncio.run(
        save_in_db(data["jobs"]),
        loop_factory=loop
)
        print(f"saved in db")


while True:
    choice = int(input("choose: "))
    if choice == 1:
        get_jobs()
    elif choice ==2:
        asyncio.run(get_remote(),loop_factory=loop)