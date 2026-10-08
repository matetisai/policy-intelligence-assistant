# Policy Intelligence Assistant

An AI-powered policy assistant that allows users to upload a company policy PDF and ask questions about its contents.

The application uses a Retrieval-Augmented Generation (RAG) workflow to retrieve relevant information from the uploaded policy before generating an answer.

## 🚀 Live Demo

**Live Application:**

https://policy-intelligence-assistant-1.onrender.com

**GitHub Repository:**

https://github.com/matetisai/policy-intelligence-assistant

## 🚀 Features

- Upload a company policy PDF
- Extract text from PDF documents
- Split policy text into smaller chunks
- Generate semantic embeddings using Gemini Embeddings
- Retrieve relevant policy sections using cosine similarity
- Generate AI-powered answers using Gemini
- Generate suggested questions based on the uploaded policy
- Ask multiple questions within the uploaded policy session
- Clear the current policy and start a new session
- Reject questions when relevant information cannot be found in the uploaded policy
- Responsive web interface accessible from desktop and mobile devices

## 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- PyPDF
- NumPy
- Requests

### AI / Machine Learning

- Google Gemini API
- Gemini Embeddings (`gemini-embedding-001`)
- Gemini (`gemini-3.1-flash-lite`)
- Cosine similarity for semantic retrieval

### Frontend

- HTML
- CSS
- JavaScript

### Deployment & Development

- Render
- Git
- GitHub
- VS Code

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation (RAG) workflow:

1. The user uploads a policy PDF.
2. The backend extracts text from the PDF using PyPDF.
3. The extracted text is divided into smaller chunks.
4. Gemini Embeddings converts the policy chunks into numerical embeddings.
5. The user's question is also converted into an embedding.
6. The system calculates cosine similarity between the question embedding and policy chunk embeddings.
7. The most relevant policy chunks are retrieved.
8. The retrieved policy information is provided to Gemini.
9. Gemini generates an answer using only the retrieved policy information.
10. If relevant information cannot be found, the assistant informs the user that the information is not available in the uploaded policy.

## 📁 Project Structure

```text
policy-intelligence-assistant/
│
├── backend/
│   ├── main.py
│   ├── chunking.py
│   ├── embeddings.py
│   │
│   └── frontend/
│       ├── index.html
│       └── style.css
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/matetisai/policy-intelligence-assistant.git

### 2. Open the project

```bash
cd policy-intelligence-assistant

### 3. Create a virtual environment

```bash
python -m venv venv

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\activate

### 5. Install dependencies

```powershell
pip install -r requirements.txt

### 6. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here

### 7. Start the backend

```powershell
uvicorn backend.main:app --reload

http://127.0.0.1:8000

http://127.0.0.1:8000/docs

### 8. Start the frontend

Open another terminal and run:

```powershell
python -m http.server 5500 --directory backend/frontend

http://127.0.0.1:5500

## 💡 Example Questions

After uploading a policy, users can ask questions such as:

- What are the password security requirements?
- How should I report a security incident?
- What are the rules for remote work?
- What are the travel expense limits?
- What documentation is required for expense reimbursement?

The suggested questions are automatically generated based on the uploaded policy.

## 🔒 Policy-Based Answers

The assistant is designed to answer questions using information retrieved from the uploaded policy.

If relevant information cannot be found in the uploaded policy, the assistant informs the user that the information could not be found.

## 🌐 Deployment

The application is deployed using Render.

### Backend

The FastAPI backend is deployed as a Render Web Service.

### Frontend

The HTML, CSS, and JavaScript frontend is deployed as a Render Static Site.

The frontend communicates with the deployed FastAPI backend through REST API endpoints.

## 🔮 Future Improvements

- Support multiple policy documents
- Add user authentication
- Add policy version management
- Add source citations for answers
- Add a production-ready vector database
- Improve document processing for scanned PDFs
- Add document metadata and policy categories
- Improve AI response validation
- Add persistent conversation history
- Add automated testing
- Add monitoring and logging

## 👨‍💻 Author

**Mateti Sai**

B.Sc. Computer Science Graduate

GitHub:

https://github.com/matetisai