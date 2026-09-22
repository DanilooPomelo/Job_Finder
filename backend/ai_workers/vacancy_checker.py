#from backend.logic import 
from backend.database import as_session, engine
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from backend.model import Job, AiJob
from sqlalchemy.dialects.postgresql import insert as pg_insert
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
from backend.logic import timer_time

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

async def get_jobs_for_AI():
    async with as_session() as s:
        jobs_ai = []
        q = (select(AiJob).options(selectinload(AiJob.job)).where(AiJob.status=="new"))
        jobs = (await s.scalars(q)).all()
        for jobi in jobs:
            jobi.status = "processing"
            #print(f"{jobi.job.id}|{jobi.job.title}")
            jobs_ai.append({"rew_id":jobi.id,
                            "job_id":jobi.job_id,
                            "ai_status":jobi.status,
                            "scoring":jobi.match_score,
                            "j_title":jobi.job.title,
                            "company":jobi.job.company,
                            "location":jobi.job.location,
                            "snippet":jobi.job.snippet 
                            })
        await s.commit()
        
        return jobs_ai
@timer_time
async def data_for_check():
    
    vacs = await get_jobs_for_AI()
    for vac in vacs:
        ai_vac = {
                    "ai_status":vac['ai_status'],
                    "scoring":vac["scoring"],
                    "j_title":vac['j_title'],
                    "company":vac['company'],
                    "location":vac['location'],
                    "snippet":vac['snippet'] 
                } 
        result = await ai_godvbless(ai_vac)
        print(result)

    
       
    #return ai_vac

async def ai_godvbless(job_v):
    

    response = await client.chat.completions.create(
        model="openrouter/free",
        messages=[{
            "role": "system",
            "content":"""You are an AI job-matching assistant.

Your task is to evaluate how well a job vacancy matches the candidate profile below.

CANDIDATE PROFILE

Target roles:


* Junior Python Developer
* Junior Python Backend Developer
* Junior Backend Developer
* Junior Backend Engineer
* Junior Python Software Engineer

Location preferences:

* Remote positions
* Moldova-based positions
* Do not reject a vacancy only because it is outside Moldova if the position is remote.
* The candidate does not want positions that require Romanian.

Technical skills:

* Python
* SQL
* PostgreSQL
* SQLite
* SQLAlchemy
* FastAPI
* REST API
* asyncio
* OOP
* CRUD
* Relational databases
* Git
* GitHub
* PySide6
* Qt Designer

Currently learning:

* Django
* React
* More advanced backend development and REST API concepts

Languages:

* English: B1
* Russian: B2
* Ukrainian: B2
* Polish: B2

Education:

* IT engineering degree

MATCHING RULES

1. Evaluate the vacancy using only the information provided in the vacancy.
2. Focus primarily on Python, backend development, APIs, databases and the actual requirements of the position.
3. Do not require the candidate to match every technology in the vacancy.
4. Distinguish between required skills and optional/preferred skills.
5. Missing optional skills should have much less impact than missing required skills.
6. A vacancy can still be a good match when the candidate does not know some technologies, especially when they are not core requirements.
7. Strongly reduce the match when the vacancy requires senior-level experience, extensive years of professional experience, or technologies fundamentally unrelated to the candidate's target.
8. Reject or strongly penalize a vacancy when Romanian is explicitly required.
9. Do not invent candidate skills or experience that are not listed in the profile.
10. Give a final match score from 0 to 100.
11. Consider the vacancy suitable for the candidate when the final match is 60 or higher.

Return your assessment with exactly these fields:

status
match_score
reason
missing_skills

Where:

* status must be either "accepted" or "rejected"
* match_score must be an integer from 0 to 100
* reason must briefly explain why the vacancy matches or does not match
* missing_skills must contain the important required skills that the candidate appears to lack. If there are none, return an empty string.
"""
        },
        {
            "role":"user",
            "content":str(job_v)
        }
        ]

    )
    res = response.choices[0].message.content
    return res


        
