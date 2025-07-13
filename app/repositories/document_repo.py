from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(db:Session, document:Document):
    db.add(document)
    db.commit()
    db.refresh(document)
    return document 

def get_document_by_id(db:Session, id:int):
    return db.query(Document).filter(Document.id == id).first()

def get_document_by_user_id(db:Session, user_id:int):
    return db.query(Document).filter(Document.user_id == user_id).all()

def delete_document(db:Session, document:Document):
    db.delete(document)
    db.commit()