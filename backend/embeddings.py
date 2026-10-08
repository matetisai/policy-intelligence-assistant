import os
import requests
import numpy as np


def create_embedding(text):
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": os.getenv("GEMINI_API_KEY")
        },
        json={
            "model": "models/gemini-embedding-001",
            "content": {
                "parts": [
                    {
                        "text": text
                    }
                ]
            }
        },
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return np.array(
        result["embedding"]["values"],
        dtype=np.float32
    )


def create_embeddings(chunks):
    embeddings = []

    for chunk in chunks:
        embedding = create_embedding(chunk)
        embeddings.append(embedding)

    return np.array(embeddings)


def find_best_chunks(question, chunks, embeddings, top_k=3):

    question_embedding = create_embedding(question)

    scores = np.dot(
        embeddings,
        question_embedding
    ) / (
        np.linalg.norm(embeddings, axis=1)
        * np.linalg.norm(question_embedding)
    )

    top_indices = np.argsort(scores)[-top_k:][::-1]

    best_chunks = [
        chunks[i]
        for i in top_indices
    ]

    best_score = float(
        scores[top_indices[0]]
    )

    return best_chunks, best_score