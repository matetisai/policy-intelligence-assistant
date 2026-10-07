# Policy Intelligence Assistant

An AI-powered policy assistant that allows users to upload a company policy PDF and ask questions about its contents.

The application uses Retrieval-Augmented Generation (RAG) to find relevant information from the uploaded policy before generating an answer.

## 🚀 Features

- Upload a policy PDF
- Extract text from PDF documents
- Split policy text into smaller chunks
- Generate semantic embeddings using Sentence Transformers
- Retrieve relevant policy sections for a user's question
- Generate answers using Llama 3.2
- Generate suggested questions from the uploaded policy
- Maintain multiple questions and answers in a chat interface
- Clear the current policy and start a new session

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- PyPDF
- Sentence Transformers
- NumPy
- Ollama

### AI / Machine Learning
- Sentence Transformers
- `all-MiniLM-L6-v2`
- Llama 3.2 3B

### Frontend
- HTML
- CSS
- JavaScript

### Development Tools
- Git
- GitHub
- VS Code

## 🧠 How It Works

The application follows a Retrieval-Augmented Generation (RAG) workflow:

1. The user uploads a policy PDF.
2. The backend extracts the text from the PDF.
3. The text is divided into smaller chunks.
4. Sentence Transformers converts the chunks into embeddings.
5. The user's question is converted into an embedding.
6. The system compares the question with the policy chunks using similarity scoring.
7. The most relevant policy chunks are retrieved.
8. The retrieved information is provided to Llama 3.2.
9. The AI generates an answer using the retrieved policy information.

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
├── .gitignore
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

### 5. Install the required packages

```bash
pip install fastapi uvicorn pypdf python-multipart sentence-transformers ollama

### 6. Install Ollama and download the model

```bash
ollama pull llama3.2:3b

### 7. Start the backend

```bash
fastapi dev backend/main.py

http://127.0.0.1:8000

http://127.0.0.1:8000/docs

### 8. Start the frontend

```bash
python -m http.server 5500 --directory backend/frontend

Then open:

```text
http://127.0.0.1:5500

## 💡 Example Questions

After uploading a policy, users can ask questions such as:

- What should I do if I receive a phishing email?
- How should I report a security incident?
- Can I work remotely without using a VPN?
- How should confidential data be stored?
- What are the password security requirements?

## 🔒 Policy-Based Answers

The assistant is designed to answer questions using information retrieved from the uploaded policy rather than relying on general knowledge.

If relevant information cannot be found in the uploaded policy, the assistant indicates that the information could not be found.

## 🔮 Future Improvements

- Deploy the application publicly
- Add user authentication
- Support multiple policy documents
- Add policy version management
- Improve document processing
- Add conversation history
- Add citations showing the source section of an answer
- Add a production-ready vector database
- Improve AI response validation

## 👨‍💻 Author

**Mateti Sai**

B.Sc. Computer Science Graduate

GitHub: https://github.com/matetisai