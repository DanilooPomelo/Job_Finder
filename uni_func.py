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

async def retry_func(fnc_name,*args, **kwargs):
    tryes = [2,4,6]
    for tr in tryes:
        try:
           res = await fnc_name(*args, **kwargs)
           return res 
        except (RETRY_DB_ERR) as e:
            res = e
            await asyncio.sleep(tr)
    return res



RETRY_DB_ERR = (psycopg.errors.ConnectionException,psycopg.errors.SqlclientUnableToEstablishSqlconnection,psycopg.errors.ConnectionDoesNotExist,psycopg.errors.ConnectionFailure,psycopg.errors.CannotConnectNow,psycopg.errors.AdminShutdown,psycopg.errors.CrashShutdown,psycopg.errors.ConnectionTimeout,psycopg.errors.SerializationFailure,psycopg.errors.DeadlockDetected,psycopg.errors.LockNotAvailable,psycopg.errors.TooManyConnections,
                    openai.APIConnectionError,
    openai.APITimeoutError,
    openai.RateLimitError,
    openai.InternalServerError,
)