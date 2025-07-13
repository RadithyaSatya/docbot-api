from pydantic import BaseModel


class AskRequest(BaseModel):
    question:str

    class Config:
        json_schema_extra={
            "example":{
                "question":"Siapa yang menulis dokumen ini?"
            }
        }