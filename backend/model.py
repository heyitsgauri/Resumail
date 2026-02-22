from pydantic import BaseModel

class EmailRequest(BaseModel):
    resume_text:str
    job_position:str