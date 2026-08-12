import httpx
from urllib.parse import quote
from dotenv import load_dotenv
import os
load_dotenv()


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
print(response.status_code)
print(response.text[:300])
data = response.json()
print(data["totalCount"])

for job in data["jobs"][:5]:
    print(job["title"], "-" , job["company"])

