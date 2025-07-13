import datetime
import os
import shutil
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.user import User
from app.repositories import document_repo
from app.services import embedder, parser


UPLOAD_FOLDER = "data/uploaded"

def upload_document(file: UploadFile, current_user: User, db: Session):
    if not file.filename.endswith((".pdf",".txt")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must be PDF ot TXT")
    
    filename = f"{current_user.username}_{int(datetime.datetime.utcnow().timestamp())}_{file.filename}"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        text = parser.extract_text_from_pdf(save_path)
    else:
        text = parser.extract_text_from_txt(save_path)

    if not text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File not contain text")
    
    name_only, ext = os.path.splitext(file.filename)
    new_document = Document(
        user_id = current_user.id,
        filename = filename,
        content = name_only
    )

    document_repo.create_document(db, new_document)

    chunks = parser.split_text_to_chunks(text)
    embeddings = embedder.embed_chunks(chunks)
    embedder.save_embedding(new_document.id, chunks=chunks, embeddings=embeddings)

    return new_document


def delete_data_document(doc_id: int, current_user:User, db:Session):
    document = document_repo.get_document_by_id(db, doc_id)

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    if document.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to delete this document")
    
    file_path = os.path.join(UPLOAD_FOLDER, document.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    embedder.delete_embedding
    document_repo.delete_document(db, document)