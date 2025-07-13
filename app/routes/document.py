from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories import document_repo, history_repo
from app.schemas.ask import AskRequest
from app.services.auth import get_current_user
from app.services.ask import ask_question
from app.services.upload import delete_data_document, upload_document


router = APIRouter(
    prefix="/document",
    tags=["Document"],
    dependencies=[Depends(get_current_user)]
)

@router.get("")
def get_documents(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    documents = document_repo.get_document_by_user_id(db, current_user.id)
    return{
        "message":"Get documents sucessfully",
        "documents":documents
    }

@router.post("/upload")
def upload(
    file: UploadFile,
    db: Session =Depends(get_db),
    current_user = Depends(get_current_user)
):
    document = upload_document(file, current_user, db)
    return{
        "message":"Document successfully uploaded", 
        "document":document
    }

@router.post("/{id}")
def get_document(id:int, db:Session = Depends(get_db)):
    document = document_repo.get_document_by_id(db, id)
    return{
        "message":"get document successfully",
        "document":document
    }

@router.post("/{id}/ask")
def ask_document(id:int, body:AskRequest, db:Session=Depends(get_db)):
    result = ask_question(id,body.question,db)
    return{
        "message": "Ask successfully",
        "question":result['question'],
        "answer":result['answer']
    }

@router.get("/{id}/history")
def get_history(id:int, db: Session = Depends(get_db)):
    history = history_repo.get_history_by_document_id(db,id)
    return{
        "message":"Get history successfully",
        "dialogs":history
    }

@router.delete("/{id}")
def delete_document(id:int, db:Session=Depends(get_db), current_user=Depends(get_current_user)):
    delete_data_document(id, current_user, db)
    return{
        "message":"Delete document data successfully"
    }