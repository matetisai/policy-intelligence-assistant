from sentence_transformers import SentenceTransformer
import numpy as np

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


def create_embeddings(chunks):
    model = get_model()

    return model.encode(
        chunks,
        normalize_embeddings=True
    )


def find_best_chunks(question, chunks, embeddings, top_k=3):
    model = get_model()

    question_embedding = model.encode(
        [question],
        normalize_embeddings=True
    )[0]

    scores = np.dot(embeddings, question_embedding)

    top_indices = np.argsort(scores)[-top_k:][::-1]

    best_chunks = [chunks[i] for i in top_indices]

    best_score = float(scores[top_indices[0]])

    return best_chunks, best_score