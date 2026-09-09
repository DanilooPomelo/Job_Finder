import selectors
import asyncio
import math
import time

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
    timeouts = [2,4,6]
    for t in timeouts:

        try:
            result = await func(*args, **kwargs)
            return result
    
        except Exception as e:
            await asyncio.sleep(t)
        
    print(f"Error - {e}")


