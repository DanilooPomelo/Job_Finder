import selectors
import asyncio
import math
import time
import httpx

loop = lambda:asyncio.SelectorEventLoop(selectors.SelectSelector())

def paggination(tcount: float|int , a: int):
    
    if tcount > a:
        max_pages = math.ceil(tcount / a)
        print(f"{max_pages} - страниц")

        
        return range(2, max_pages +1)
    else: 
        return range(2,2)


def jpagination():
    max_page = 15
    return range(2, max_page)

def get_for_search():
    search = input("Search Job: ")
    return search

async def timeouts_src(func, *args, **kwargs):
    fr = [429, 500,502,503,504]
    nr = [403,404,400]
    timeouts = [2,4,6]
    for t in timeouts:
        try:
            result = await func(*args, **kwargs)
            if result in fr:
                await asyncio.sleep(t)
                continue
            else: 
                return result
                
                    
            
        except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError) as e:
                result = e
                await asyncio.sleep(t)
        return result


