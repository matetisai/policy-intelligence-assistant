from fastapi import FastAPI, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io
import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")

def generate_suggested_questions(text):
    prompt = f"""
You are helping a user explore an uploaded policy document.

Based ONLY on the document below, generate 3 useful questions
that a user would naturally want to ask about this document.

Rules:
1. Use ONLY information found in the document.
2. Do not invent topics that are not present.
3. Make each question different.
4. Questions should cover different parts of the document.
5. Keep each question short and clear.
6. Return ONLY the questions, one per line.
7. Do not number the questions.
8. Do not use bullet points.

Document:
{text}
"""

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": os.getenv("GEMINI_API_KEY")
        },
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        },
        timeout=60
    )

    if response.status_code != 200:
       return []

    result = response.json()

    if "candidates" not in result:
        return []

    questions_text = result["candidates"][0]["content"]["parts"][0]["text"]

    questions = [
        q.strip()
        for q in questions_text.split("\n")
        if q.strip()
    ]

    return questions[:3]


from chunking import split_text
from embeddings import create_embeddings, find_best_chunks

app = FastAPI(title="Policy Intelligence Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for user sessions
sessions = {}

@app.get("/")
def home():
    return {
        "message": "Policy Intelligence Assistant API is running!"
    }


@app.post("/upload-policy")
async def upload_policy(
    file: UploadFile = File(...),
    session_id: str = Header(...)
):

    contents = await file.read()

    if not contents:
        return {
            "error": "The uploaded PDF is empty."
        }

    pdf_file = io.BytesIO(contents)

    try:
        reader = PdfReader(pdf_file)
    except Exception:
        return {
            "error": "The uploaded file could not be read as a valid PDF."
        }

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    if not text.strip():
        return {
            "error": "The PDF does not contain readable text."
        }

    chunks = split_text(text)
    embeddings = create_embeddings(chunks)

    suggested_questions = generate_suggested_questions(text)

    sessions[session_id] = {
        "text": text,
        "chunks": chunks,
        "embeddings": embeddings,
        "suggested_questions": suggested_questions
    }

    return {
        "filename": file.filename,
        "pages": len(reader.pages),
        "chunks": len(chunks),
        "suggested_questions": suggested_questions
    }


@app.post("/ask")
async def ask_question(
    question: str,
    session_id: str = Header(...)
):

    session = sessions.get(session_id)

    if not session:
        return {
            "answer": "Please upload a policy PDF first."
        }

    best_chunks, score = find_best_chunks(
        question,
        session["chunks"],
        session["embeddings"]
    )

    print("Similarity score:", score)

    if score < 0.15:
        return {
            "answer": "I could not find relevant information in the uploaded policy."
        }

    policy_info = "\n\n".join(best_chunks)

    prompt = f"""
You are a policy assistant.

Answer the user's question using ONLY the policy information provided below.

Policy information:
{policy_info}

User question:
{question}

Follow these rules strictly:

1. Answer the user's question directly using the provided policy information.

2. Carefully read ALL of the provided policy information before answering.

3. If the policy information contains the answer, you MUST provide the answer.
   Do not say that the information is missing when the answer is present in the provided policy information.

4. Use only information explicitly stated in the provided policy information.
   Do not use general knowledge, assumptions, or information from outside the policy.

5. You may summarize or combine information from different parts of the provided policy information
   as long as the answer remains faithful to the policy.

6. Do not invent policy numbers, section names, dates, limits, rules, procedures, or other details.

7. If you mention a policy section, use its name or number ONLY if it appears explicitly in the provided policy information.

8. Only say:
"I could not find this information in the uploaded policy."
when the answer is genuinely not present anywhere in the provided policy information.

9. If the question asks for a list, provide the complete list when the policy provides one.

10. Give a short, clear, and direct answer.


11. When the answer contains multiple requirements, actions, or items, use short bullet points to make the answer easy to read.

12. Do not use unnecessary introductions, conclusions, or explanations.

13. Keep the answer concise and use the terminology from the policy.

Answer:
"""

    response = requests.post(
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent",
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": os.getenv("GEMINI_API_KEY")
    },
    json={
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    },
    timeout=60
)
    if response.status_code != 200:
        return {
        "answer": "Gemini is temporarily unavailable. Please try again in a moment.",
        "similarity_score": float(score)
    }

    result = response.json()

    if "candidates" not in result:
        return {
            "answer": "Gemini could not generate an answer. Please try again.",
            "similarity_score": float(score)
        }

    answer = result["candidates"][0]["content"]["parts"][0]["text"]

    return {
        "answer": answer,
        "similarity_score": float(score)
    }
