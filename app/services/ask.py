from fastapi import HTTPException, status
from app.models.history import History
from app.repositories import document_repo, history_repo
from sqlalchemy.orm import Session

from app.services.llm import ask_llm
from app.services.qa_engine import find_most_relevant_chunk


def ask_question(doc_id: int, question: str, db:Session):
    doc = document_repo.get_document_by_id(db, doc_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    context = find_most_relevant_chunk(question, doc_id)
    answer = ask_llm(question, context)

    new_history = History(
        question = question,
        answer = answer,
        document_id = doc_id
    )
    history_repo.create_history(db, new_history)

    return{
        "question": question,
        "answer":answer
    }