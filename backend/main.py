from fastapi import FastAPI, UploadFile, File, Header
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io
import ollama
def generate_suggested_questions(text):
    prompt = f"""
You are generating suggested questions for an employee policy assistant.

Read the policy text below and create EXACTLY 6 questions that an employee could ask about this policy.

STRICT RULES:

- Every line MUST be a question.
- Every line MUST end with a question mark (?).
- Start each question with words such as:
  What, How, Who, When, Where, Which, Can, or Are.
- Do NOT write statements.
- Do NOT copy sentences from the policy.
- Do NOT give answers.
- Do NOT add explanations.
- Do NOT number the questions.
- Return ONLY 6 questions, one question per line.
- Use ONLY information that appears in the policy.
- Choose questions from different topics or sections of the policy.
- Avoid asking multiple questions about the same topic.
- Prefer questions that cover different useful areas of the policy.
- Only ask questions that can be answered directly using information stated in the policy.
- Do not ask about consequences, penalties, reasons, opinions, or other information unless the policy explicitly provides that information.

Good example:
What should an employee do if company equipment is lost or stolen?
How should an employee report a security incident?
What should employees do if they suspect unauthorized access?

Bad example:
Employees must report lost equipment.
The company requires employees to use VPN.
Employees should change their passwords.

Policy text:
{text[:6000]}
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    questions = response["message"]["content"].strip().split("\n")

    questions = [
        q.strip()
        for q in questions
        if q.strip().endswith("?")
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
        "text": text,
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

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response["message"]["content"],
        "similarity_score": float(score)
    }