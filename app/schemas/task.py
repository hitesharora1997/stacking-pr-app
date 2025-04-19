from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    is_completed: bool = False
