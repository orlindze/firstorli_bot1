import logging 

logger = logging.getLogger(__name__)



from pydantic import BaseModel

class Fighter(BaseModel):
    name: str    
    style: str   