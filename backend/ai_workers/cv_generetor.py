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

"""

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("CV_GENERATOR_API"),
)



async def get_for_cv():
    async with as_session() as s:
        cv_gen = []
        q = (select(AiJob).options(selectinload(AiJob.job)).where(AiJob.status == "accepted"))
        jobs = (await s.scalars(q)).all()
        for j in jobs:
            cv_gen.append({
                "req_id":j.id,
                "scoring":j.match_score,
                "title":j.job.title,
                "company":j.job.company,
                "snippet":j.job.snippet,
                "location":j.job.location,
                "m_skills":j.missingskills,
                "reason":j.reason

            })
        return cv_gen

async def ai_gen_cv(vac):
    resp = await client.chat.completions.create(
        model="openrouter/free",
                messages=[{
                    "role": "system",
                    "content":PROMPT
                },
                {
                    "role":"user",
                    "content":str(vac)
                }
                ]
    )
    res = resp.choices[0].message.content
    res = res.replace("```json", "").replace("```", "").strip()
    result = json.loads(res)
    return result

async def save_cv():
    pass

    