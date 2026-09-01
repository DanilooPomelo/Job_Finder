import selectors
import asyncio
import math

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