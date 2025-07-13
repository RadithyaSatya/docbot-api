from sqlalchemy.orm import Session

from app.models.history import History

def create_history(db: Session, history: History):
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_history_by_document_id(db:Session, document_id: id):
    return db.query(History).filter(History.document_id == document_id).all()