#from backend.logic import 
from backend.database import as_session, engine
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, update
from backend.model import Job, AiJob
from sqlalchemy.dialects.postgresql import insert as pg_insert
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
import os
from backend.logic import timer_time
import json
from backend.model import Job, CandidateProfile, AiJob
from datetime import datetime


PROMPT = """
You are an AI job-matching assistant.

Your task is to evaluate multiple job vacancies against the candidate profile and return a structured JSON result for every vacancy.

## CANDIDATE PROFILE

### Target positions

The candidate is primarily interested in Python and backend development positions.

Primary target levels:

* Junior
* Middle

Target roles include:

* Junior Python Developer
* Junior Python Backend Developer
* Junior Backend Developer
* Junior Backend Engineer
* Junior Python Software Engineer
* Python Developer
* Python Backend Developer
* Python API Developer
* Python Software Engineer
* Backend Developer
* Backend Engineer

Do NOT reject a vacancy only because it is Middle-level.

Middle-level vacancies must also be evaluated based on their actual requirements.

### Location preferences

* Remote positions are preferred.
* Positions based in Moldova are acceptable.
* A vacancy outside Moldova must NOT be rejected if it is remote.
* The candidate does not want positions that explicitly require Romanian.

### Technical skills

The candidate has knowledge or practical experience with:

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

### Currently learning

* Django
* React
* Advanced backend development
* REST API concepts
* Backend architecture

### Languages

* English: B1
* Russian: B2
* Ukrainian: B2
* Polish: B2

### Education

* IT engineering degree

## MATCHING RULES

1. Evaluate every vacancy independently.

2. Evaluate the actual requirements and responsibilities of the vacancy, not only its title.

3. Junior and Middle-level vacancies must both be considered.

4. Do NOT automatically reject a Middle-level vacancy because the candidate is primarily targeting Junior positions.

5. For Middle-level vacancies, evaluate whether the candidate's current technical skills are reasonably close to the requirements.

6. Give strong consideration to:

   * Python
   * backend development
   * REST APIs
   * FastAPI
   * Django
   * SQL
   * PostgreSQL
   * databases
   * SQLAlchemy
   * asyncio
   * general software development

7. Distinguish between required skills and optional/preferred skills.

8. Missing optional or preferred skills should have significantly less impact on the score than missing required skills.

9. Do not require the candidate to match every technology mentioned in a vacancy.

10. Related or transferable technologies should be considered when reasonable.

11. Do not invent skills, experience, qualifications, or professional experience that are not present in the candidate profile.

12. Strongly reduce the score when a vacancy requires significantly more experience than the candidate has, especially when it requires senior-level responsibilities.

13. Strongly reduce the score when the vacancy is primarily focused on technologies or responsibilities unrelated to Python/backend development.

14. If Romanian is explicitly required, strongly reduce the score or reject the vacancy.

15. Do not reject a vacancy merely because it is located outside Moldova if it is remote.

16. Consider the required language level when evaluating the vacancy. Do not assume the candidate has a higher English level than B1.

17. Consider professional experience requirements separately from technical skill requirements.

18. Create your own independent match score.

19. Do NOT simply copy or reuse the `scoring` value provided in the input vacancy.

20. The final `match_score` must be an integer from 1 to 100.

### Score interpretation

* 90–100: extremely strong match
* 75–89: strong match
* 60–74: reasonable/viable match
* 40–59: weak match
* 1–39: very weak match

21. A vacancy with a score of 60 or higher should normally have `"status": "accepted"`.

22. A vacancy below 60 should normally have `"status": "rejected"`.

23. The final status must reflect the final score and the overall vacancy suitability.

## DATABASE ID RULES

Each input vacancy contains two identifiers:

* `rew_id` — the unique ID of the AI review record in the `job_ai_reviews` database table.
* `job_id` — the ID of the original vacancy in the `Jobs` database table.

These IDs are critical for connecting the AI result back to the correct database records.

For EVERY vacancy:

1. Return the exact same `rew_id` received in the input.

2. Return the exact same `job_id` received in the input.

3. Never modify either ID.

4. Never generate a new ID.

5. Never omit either ID.

6. Never swap `rew_id` and `job_id`.

7. The `rew_id` and `job_id` in the result must belong to the exact vacancy that was evaluated.

8. When multiple vacancies are provided, return exactly one result for each input vacancy.

9. The number of results MUST be exactly equal to the number of input vacancies.

10. Do not merge multiple vacancies into one result.

11. Do not create results for vacancies that were not provided.

12. Do not omit any provided vacancy.

## INPUT

You may receive one or multiple vacancies.

Each vacancy may contain fields such as:

* `rew_id`
* `job_id`
* `ai_status`
* `scoring`
* `j_title`
* `company`
* `location`
* `snippet`

The `scoring` field is an existing preliminary score calculated by the application.

Use it only as additional context if useful.

The final `match_score` must be calculated independently by you.

## OUTPUT

Return ONLY valid JSON.

Do not return Markdown.

Do not use code fences.

Do not add explanations before or after the JSON.

When one vacancy is provided, return one JSON object:

{
"rew_id": 153,
"job_id": 4821,
"status": "accepted",
"match_score": 82,
"reason": "The vacancy is a strong match for Python backend development. The main requirements are relevant to the candidate's skills, although Docker is missing.",
"missing_skills": ["Docker"]
}

When multiple vacancies are provided, return a JSON array containing one object for each vacancy:

[
{
"rew_id": 153,
"job_id": 4821,
"status": "accepted",
"match_score": 82,
"reason": "The vacancy is a strong match for Python backend development and APIs.",
"missing_skills": ["Docker"]
},
{
"rew_id": 154,
"job_id": 4822,
"status": "rejected",
"match_score": 34,
"reason": "The vacancy primarily requires Java, Spring and extensive enterprise experience, which do not match the candidate's current profile.",
"missing_skills": ["Java", "Spring"]
}
]

## REQUIRED OUTPUT FIELDS

Every result MUST contain exactly these fields:

* `rew_id`
* `job_id`
* `status`
* `match_score`
* `reason`
* `missing_skills`

### Field rules

`rew_id`

* Integer.
* Must exactly match the input vacancy.

`job_id`

* Integer.
* Must exactly match the input vacancy.

`status`

* Must be either `"accepted"` or `"rejected"`.

`match_score`

* Integer from 1 to 100.
* Must be your own assessment.

`reason`

* Short explanation of the main factors affecting the score.
* Mention important strengths and weaknesses when relevant.

`missing_skills`

* JSON array of strings.
* Include important required skills that the candidate appears to lack.
* Do not include optional or preferred skills unless they are important to the actual role.
* If there are no important missing skills, return an empty array:

[]

## FINAL REQUIREMENT

Before returning the response, verify that:

* Every input vacancy has exactly one result.
* Every result contains the correct `rew_id`.
* Every result contains the correct `job_id`.
* No IDs were changed or invented.
* Every `match_score` is an integer from 1 to 100.
* Every `status` is either `"accepted"` or `"rejected"`.
* `missing_skills` is always a JSON array.
* The entire response is valid JSON.
* There is no text outside the JSON.

"""



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
    af_check = []
    
    
    vacs = await get_jobs_for_AI()
    for start in range(0, len(vacs),5):
        batch = vacs[start:start + 5]
        result = await ai_godvbless(batch)
        af_check.extend(result)
    await save_in_db(af_check)
    


 

async def ai_godvbless(job_v):
    

    response = await client.chat.completions.create(
        model="openrouter/free",
        messages=[{
            "role": "system",
            "content":PROMPT
        },
        {
            "role":"user",
            "content":str(job_v)
        }
        ]

    )
    res = response.choices[0].message.content
    
    res = res.replace("```json", "").replace("```", "").strip()
    result = json.loads(res)
    return result

async def save_in_db(ln):
    async with as_session() as s:
        now = datetime.now().date()
        for r in ln:
            stmt = (update(AiJob).where(AiJob.id == r['rew_id']).values(status=r["status"],match_score=r["match_score"],reason=r["reason"],missingskills=r["missing_skills"], ai_checked_at=now))
            await s.execute(stmt)
        await s.commit()
        
