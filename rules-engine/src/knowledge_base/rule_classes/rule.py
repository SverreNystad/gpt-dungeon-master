from pydantic import BaseModel

class Rule(BaseModel):

    """
    Rule class is the parent class for all rules.

    It is used to 
    """

    id: str
    # name: str
    type: str
    description: str