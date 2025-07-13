import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(question:str, context:str)->str:
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages = [
            {
                "role" : "system",
                "content": "Kamu adalah AI yang menjawab pertanyaan berdasdarkan dokumen. Jawaban harus jelas dan akurat. Kembangkan bahasanya supaya mudah di mengerti"
            },
            {
                "role":"user",
                "content": f"Pertanyaan: {question}\n\n dokumen:{context}"
            }
        ],
        temperature=0.2,
        max_tokens=256
    )
    return response.choices[0].message.content.strip()