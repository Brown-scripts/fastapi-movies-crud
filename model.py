from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
    id: int
    Title: str
    Year: int
    #storyline: Optional[str]=None